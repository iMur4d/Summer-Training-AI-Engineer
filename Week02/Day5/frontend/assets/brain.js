// ==========================================
// CONFIGURATION
// ==========================================
const LOBE_COLORS = {
    'frontal': { r: 92, g: 225, b: 230 },
    'occipital': { r: 217, g: 70, b: 239 },
    'temporal': { r: 255, g: 158, b: 0 },
    'cerebellum': { r: 0, g: 255, b: 128 },
    'stem': { r: 255, g: 255, b: 255 }
};
const DEFAULT_COLOR = { r: 40, g: 160, b: 210 };
const PROJECT_DEFAULT_COLOR = { r: 60, g: 240, b: 255 };

const defaultCameraPos = new THREE.Vector3(0, 0, 800);
const defaultOrbitCenter = new THREE.Vector3(0, 0, 0);

// ==========================================
// DATA MODEL
// ==========================================
// Generic Knowledge Object for future extensibility (Semantic Search, AI, RAG)
class KnowledgeObject {
    constructor(data) {
        this.id = data.id;
        this.title = data.title || "Untitled";
        this.date = data.date || "Unknown Date";
        this.tags = data.tags || [];
        this.raw_content = data.raw_content || "";
        this.lobe = data.lobe || "frontal";
        
        // Extensible generic metadata store for future v0.8+ integrations
        this.metadata = {
            semanticVector: [],
            aiInsights: [],
            relatedNotes: []
        };
    }
}

// Data injected from Streamlit
const graphData = typeof window !== 'undefined' ? {{ GRAPH_DATA }} : {nodes:[], links:[]};
const vaultKnowledge = (graphData.nodes || []).map(n => new KnowledgeObject(n));
const vaultLinks = graphData.links || [];

// ==========================================
// THREE.JS SCENE
// ==========================================
const canvas = document.getElementById('webgl-canvas');
const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);

const scene = new THREE.Scene();
const brainGroup = new THREE.Group();
scene.add(brainGroup);
brainGroup.rotation.x = 0.15;
brainGroup.rotation.y = -0.5;

// ==========================================
// CAMERA & CONTROLS
// ==========================================
const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 4000);
camera.position.copy(defaultCameraPos);

let isMemoryActive = false;
let isReturningToNetwork = false;
let targetCameraPos = defaultCameraPos.clone();
let targetOrbitCenter = defaultOrbitCenter.clone();

const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.enablePan = true;
controls.maxDistance = 2000;
controls.minDistance = 200;

function resetCamera() {
    if (isMemoryActive) return;
    isReturningToNetwork = true;
    targetCameraPos.copy(defaultCameraPos);
    targetOrbitCenter.copy(defaultOrbitCenter);
}

// ==========================================
// SHADERS
// ==========================================
const pointVS = `
uniform float uTime;
attribute vec4 aColor;
attribute float aSize;
attribute float aIsProject;
varying vec4 vColor;
varying float vIsProject;
varying float vTime;
varying float vDepthFade;
void main() {
    vColor = aColor;
    vIsProject = aIsProject;
    vTime = uTime;
    vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
    float depth = -mvPosition.z;
    // Increased atmospheric depth fog
    vDepthFade = smoothstep(1800.0, 400.0, depth);
    
    float breathe = 1.0 + 0.06 * sin(uTime * 2.0 + position.x * 0.02 + position.y * 0.03);
    float planetBreathe = 1.0 + 0.04 * sin(uTime * 0.8 + position.z * 0.01);
    float sizeMult = aIsProject > 0.5 ? planetBreathe : breathe;
    
    gl_PointSize = aSize * (800.0 / -mvPosition.z) * sizeMult; 
    gl_Position = projectionMatrix * mvPosition;
}
`;

const pointFS = `
varying vec4 vColor;
varying float vIsProject;
varying float vTime;
varying float vDepthFade;
void main() {
    vec2 uv = gl_PointCoord - 0.5;
    float r = length(uv);
    if (r > 0.5) discard;
    
    vec4 finalColor = vColor;
    if (vIsProject > 0.5) {
        vec2 sphereNormal = uv * 2.0;
        float sphereDist = length(sphereNormal);
        if (sphereDist > 1.0) discard;
        
        vec3 normal = vec3(sphereNormal, sqrt(1.0 - sphereDist * sphereDist));
        vec3 lightDir = normalize(vec3(-0.4, -0.5, 1.0));
        float diffuse = max(dot(normal, lightDir), 0.0);
        
        vec3 viewDir = vec3(0.0, 0.0, 1.0);
        vec3 halfDir = normalize(lightDir + viewDir);
        float spec = pow(max(dot(normal, halfDir), 0.0), 32.0);
        
        float limb = 1.0 - sphereDist;
        float atmosphere = smoothstep(0.0, 0.35, limb) * (1.0 - smoothstep(0.0, 0.15, limb)) * 2.5;
        float surface = smoothstep(1.0, 0.3, sphereDist);
        
        vec3 planetColor = finalColor.rgb * (0.4 + 0.6 * diffuse) + vec3(1.0) * spec * 0.5;
        vec3 atmosColor = finalColor.rgb * 1.5 + vec3(0.15);
        
        vec3 combined = planetColor * surface + atmosColor * atmosphere;
        float combinedAlpha = (surface * 0.9 + atmosphere * 0.6) * finalColor.a;
        
        gl_FragColor = vec4(combined, combinedAlpha);
    } else {
        float core = smoothstep(0.2, 0.0, r) * 1.0;
        float halo = smoothstep(0.5, 0.1, r) * 0.45;
        float outerBloom = exp(-r * 6.0) * 0.12;
        finalColor.a *= (core + halo + outerBloom);
        finalColor.rgb *= (0.85 + 0.15 * vDepthFade);
        gl_FragColor = finalColor;
    }
}
`;

const lineVS = `
uniform float uTime;
attribute vec4 aColor;
varying vec4 vColor;
varying vec3 vWorldPos;
varying float vTime;
void main() {
    vColor = aColor;
    vTime = uTime;
    vWorldPos = position;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}
`;

const lineFS = `
varying vec4 vColor;
varying vec3 vWorldPos;
varying float vTime;
void main() {
    float spatialPhase = vWorldPos.x * 0.008 + vWorldPos.y * 0.008 + vWorldPos.z * 0.008;
    float pulse = smoothstep(0.08, 0.0, abs(fract(spatialPhase + vTime * 0.3) - 0.5)) * 0.5;
    vec4 finalColor = vColor;
    finalColor.a *= (1.0 + pulse * 2.0);
    finalColor.rgb = mix(finalColor.rgb, vec3(1.0), pulse * 0.25);
    gl_FragColor = finalColor;
}
`;

// ==========================================
// BACKGROUND ENVIRONMENT
// ==========================================
const starsGeo = new THREE.BufferGeometry();
const starsCount = 2500;
const starsPos = new Float32Array(starsCount * 3);
const starsSizes = new Float32Array(starsCount);
for (let i = 0; i < starsCount; i++) {
    starsPos[i * 3] = (Math.random() - 0.5) * 3000;
    starsPos[i * 3 + 1] = (Math.random() - 0.5) * 3000;
    starsPos[i * 3 + 2] = (Math.random() - 0.5) * 3000;
    starsSizes[i] = Math.random() * 1.5 + 0.5;
}
starsGeo.setAttribute('position', new THREE.BufferAttribute(starsPos, 3));
starsGeo.setAttribute('size', new THREE.BufferAttribute(starsSizes, 1));
const starsMat = new THREE.ShaderMaterial({
    vertexShader: `
        uniform float uTime;
        attribute float size;
        void main() {
            vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
            gl_PointSize = size * (1000.0 / -mvPosition.z);
            gl_Position = projectionMatrix * mvPosition;
        }`,
    fragmentShader: `
        void main() {
            vec2 uv = gl_PointCoord - vec2(0.5);
            if(length(uv) > 0.5) discard;
            gl_FragColor = vec4(1.0, 1.0, 1.0, 0.5);
        }`,
    uniforms: { uTime: { value: 0.0 } },
    transparent: true, blending: THREE.AdditiveBlending, depthWrite: false
});
const starsMesh = new THREE.Points(starsGeo, starsMat);
scene.add(starsMesh);

// ==========================================
// BRAIN NODES & GRAPH GENERATION
// ==========================================
function computeBrainShape(r, theta, phi) {
    // Increased scale for better spacing and depth
    const RX = 165, RY = 150, RZ = 240;
    let nx = Math.sin(phi) * Math.cos(theta);
    let ny = Math.sin(phi) * Math.sin(theta);
    let nz = Math.cos(phi);

    let lobe = 'parietal';
    if (ny > 0.22 && nz > 0.2 && Math.abs(nx) < 0.45) lobe = 'cerebellum';
    else if (nz < -0.15) lobe = 'frontal';
    else if (nz > 0.36 && ny < 0.35) lobe = 'occipital';
    else if (Math.abs(nx) > 0.5 && ny > 0.0 && nz > -0.2 && nz < 0.35) lobe = 'temporal';

    let x = RX * r * nx, y = RY * r * ny, z = RZ * r * nz;

    if (lobe !== 'cerebellum') {
        let gyrusTime = 12 * theta + Math.sin(phi * 8) * 3.5;
        let ripple = 1.0 + 0.07 * Math.sin(gyrusTime) * Math.sin(phi * 14);
        x *= ripple; y *= ripple; z *= ripple;

        let zNorm = z / RZ;
        x *= (0.82 + 0.18 * zNorm - 0.05 * Math.pow(zNorm, 2));
        y *= (0.90 + 0.10 * zNorm);
    }
    return { x, y, z, lobe };
}

const logicNodes = [];
const logicEdges = [];

for (let i = 0; i < 1200; i++) {
    const r = 0.55 + 0.45 * Math.pow(Math.random(), 1 / 3);
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos((Math.random() * 2) - 1);
    const shape = computeBrainShape(r, theta, phi);

    logicNodes.push({
        origX: shape.x, origY: -shape.y, origZ: shape.z,
        isProject: false,
        knowledgeObj: null,
        lobe: shape.lobe,
        highlightColor: LOBE_COLORS[shape.lobe] || DEFAULT_COLOR,
        currentColor: { ...DEFAULT_COLOR },
        currentAlphaMult: 1.0,
        baseRadius: Math.random() * 6 + 2,
        pulseTimer: Math.random() * Math.PI * 2,
        pulseSpeed: 0.015 + Math.random() * 0.03,
        isPulsing: Math.random() > 0.7
    });
}

let noteMap = {};
vaultKnowledge.forEach(kObj => {
    let candidate = logicNodes[Math.floor(Math.random() * logicNodes.length)];
    candidate.isProject = true;
    candidate.knowledgeObj = kObj;
    candidate.lobe = kObj.lobe || candidate.lobe;
    candidate.highlightColor = LOBE_COLORS[candidate.lobe] || PROJECT_DEFAULT_COLOR;
    candidate.baseRadius = 40; // larger core for clear visibility
    noteMap[kObj.id] = candidate;
});

vaultLinks.forEach(link => {
    const source = noteMap[link.source];
    const target = noteMap[link.target];
    if (source && target) {
        logicEdges.push({ a: source, b: target, type: 'obsidian' });
    }
});

const ptGeo = new THREE.BufferGeometry();
const ptPos = new Float32Array(logicNodes.length * 3);
const ptCol = new Float32Array(logicNodes.length * 4);
const ptSize = new Float32Array(logicNodes.length);
const ptIsProj = new Float32Array(logicNodes.length);

logicNodes.forEach((node, i) => {
    ptPos[i * 3] = node.origX; ptPos[i * 3 + 1] = node.origY; ptPos[i * 3 + 2] = node.origZ;
    ptIsProj[i] = node.isProject ? 1.0 : 0.0;
});

ptGeo.setAttribute('position', new THREE.BufferAttribute(ptPos, 3));
ptGeo.setAttribute('aColor', new THREE.BufferAttribute(ptCol, 4));
ptGeo.setAttribute('aSize', new THREE.BufferAttribute(ptSize, 1));
ptGeo.setAttribute('aIsProject', new THREE.BufferAttribute(ptIsProj, 1));

const ptMat = new THREE.ShaderMaterial({
    vertexShader: pointVS, fragmentShader: pointFS,
    uniforms: { uTime: { value: 0 } },
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending
});
const pointsObj = new THREE.Points(ptGeo, ptMat);
brainGroup.add(pointsObj);

const lineGeo = new THREE.BufferGeometry();
const linePos = new Float32Array(logicEdges.length * 6);
const lineCol = new Float32Array(logicEdges.length * 8);

logicEdges.forEach((edge, i) => {
    linePos[i * 6] = edge.a.origX; linePos[i * 6 + 1] = edge.a.origY; linePos[i * 6 + 2] = edge.a.origZ;
    linePos[i * 6 + 3] = edge.b.origX; linePos[i * 6 + 4] = edge.b.origY; linePos[i * 6 + 5] = edge.b.origZ;
});
lineGeo.setAttribute('position', new THREE.BufferAttribute(linePos, 3));
lineGeo.setAttribute('aColor', new THREE.BufferAttribute(lineCol, 4));

const lineMat = new THREE.ShaderMaterial({
    vertexShader: lineVS, fragmentShader: lineFS,
    uniforms: { uTime: { value: 0 } },
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending
});
const linesObj = new THREE.LineSegments(lineGeo, lineMat);
brainGroup.add(linesObj);

// ==========================================
// WORKSPACE & MARKDOWN
// ==========================================
marked.use(markedKatex({ throwOnError: false }));
marked.setOptions({
    highlight: function (code, lang) {
        if (lang && hljs.getLanguage(lang)) {
            return hljs.highlight(code, { language: lang }).value;
        }
        return hljs.highlightAuto(code).value;
    }
});

const workspace = document.getElementById('note-workspace');

function openNote(kObj) {
    isMemoryActive = true;
    document.body.classList.add('reading-mode'); // Dims background webgl
    
    document.getElementById('ws-title').innerText = kObj.title;
    document.getElementById('ws-date').innerText = kObj.date;

    const tags = kObj.tags || [];
    document.getElementById('ws-tags').innerHTML = tags.map(t => `<span class="meta-tag">#${t}</span>`).join('');

    const rawMd = kObj.raw_content || "";
    const wordCount = rawMd.split(/\s+/).length;
    const readTime = Math.max(1, Math.ceil(wordCount / 200));
    document.getElementById('ws-time').innerText = `${readTime} min read`;

    document.getElementById('ws-content').innerHTML = marked.parse(rawMd);

    workspace.classList.add('open');
}

function closeWorkspace(e) {
    if (e) e.stopPropagation();
    workspace.classList.remove('open');
    document.body.classList.remove('reading-mode');
    isMemoryActive = false;
    selectedNode = null;
    isReturningToNetwork = true;
}

function triggerNeuron(node) {
    selectedNode = node;
    targetOrbitCenter.set(node.origX, node.origY, node.origZ);
    const nodePos = new THREE.Vector3(node.origX, node.origY, node.origZ);
    const direction = nodePos.clone().normalize();
    // Gentle cinematic zoom in, not too aggressive
    targetCameraPos.copy(nodePos).add(direction.multiplyScalar(220)); 
    openNote(node.knowledgeObj);
    document.getElementById('sidebar-nav').classList.remove('open');
    hideTooltip();
}

// ==========================================
// SIDEBAR & SEARCH
// ==========================================
function toggleSidebar() {
    document.getElementById('sidebar-nav').classList.toggle('open');
}

function filterNotes() {
    const query = document.getElementById('search-box').value.toLowerCase();
    document.querySelectorAll('.explorer-item').forEach(el => {
        const title = el.getAttribute('data-title') || "";
        const tags = el.getAttribute('data-tags') || "";
        const content = el.getAttribute('data-content') || "";
        
        // Future proofing: This can easily be swapped out with a semantic/LLM search over the KnowledgeObjects
        if (title.includes(query) || tags.includes(query) || content.includes(query)) {
            el.style.display = 'flex';
        } else {
            el.style.display = 'none';
        }
    });
}

const explorerList = document.getElementById('explorer-list');
vaultKnowledge.forEach(kObj => {
    const el = document.createElement('div');
    el.className = 'explorer-item';
    el.setAttribute('data-title', kObj.title.toLowerCase());
    el.setAttribute('data-tags', (kObj.tags || []).join(',').toLowerCase());
    el.setAttribute('data-content', (kObj.raw_content || "").toLowerCase());

    const color = LOBE_COLORS[kObj.lobe] || PROJECT_DEFAULT_COLOR;
    const rgb = `rgb(${color.r},${color.g},${color.b})`;

    el.innerHTML = `<div class="node-icon" style="background: ${rgb}; box-shadow: 0 0 8px ${rgb}"></div> ${kObj.title}`;
    el.onclick = () => {
        const node = logicNodes.find(n => n.isProject && n.knowledgeObj.id === kObj.id);
        if (node) triggerNeuron(node);
    };
    explorerList.appendChild(el);
});

// ==========================================
// EVENT HANDLERS & TOOLTIP
// ==========================================
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2(-10, -10);
let hoveredNode = null;
let selectedNode = null;

const tooltip = document.getElementById('node-tooltip');
const tooltipTitle = document.getElementById('tooltip-title');
const tooltipDate = document.getElementById('tooltip-date');
const tooltipTags = document.getElementById('tooltip-tags');

function hideTooltip() {
    tooltip.style.opacity = '0';
}

window.addEventListener('mousemove', (e) => {
    if (workspace.classList.contains('open')) {
        hideTooltip();
        return;
    }
    
    mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
    
    if (hoveredNode && hoveredNode.isProject) {
        tooltip.style.left = `${e.clientX}px`;
        tooltip.style.top = `${e.clientY}px`;
    }
});

window.addEventListener('click', (e) => {
    if (e.target.closest('#menu-toggle') || e.target.closest('#sidebar-nav') || e.target.closest('#ui-legend') || e.target.closest('#reset-camera')) return;
    if (workspace.classList.contains('open')) return;

    if (hoveredNode && hoveredNode.isProject) {
        triggerNeuron(hoveredNode);
    } else {
        hideTooltip();
    }
});

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// ==========================================
// ANIMATION LOOP
// ==========================================
const clock = new THREE.Clock();
let globalTime = 0;

function animate() {
    requestAnimationFrame(animate);

    const delta = clock.getDelta();
    const speedMult = isMemoryActive ? 0.1 : 1.0;
    globalTime += delta * speedMult;

    // Elegant Camera Transition
    if (isMemoryActive) {
        controls.target.lerp(targetOrbitCenter, 0.04);
        camera.position.lerp(targetCameraPos, 0.04);
        isReturningToNetwork = false;
    } else if (isReturningToNetwork) {
        controls.target.lerp(defaultOrbitCenter, 0.03);
        camera.position.lerp(defaultCameraPos, 0.02);
        if (camera.position.distanceTo(defaultCameraPos) < 10) {
            isReturningToNetwork = false;
        }
    }
    controls.update();

    ptMat.uniforms.uTime.value = globalTime;
    lineMat.uniforms.uTime.value = globalTime;
    starsMat.uniforms.uTime.value = globalTime;

    // Raycaster hover evaluation
    raycaster.setFromCamera(mouse, camera);
    raycaster.params.Points.threshold = 12;

    const intersects = raycaster.intersectObject(pointsObj);
    hoveredNode = null;

    if (intersects.length > 0 && !isMemoryActive) {
        for (let i = 0; i < intersects.length; i++) {
            const idx = intersects[i].index;
            const node = logicNodes[idx];
            if (node && node.isProject) {
                hoveredNode = node;
                break;
            }
        }
    }
    
    // Tooltip logic
    if (hoveredNode && hoveredNode.isProject && !isMemoryActive) {
        tooltipTitle.innerText = hoveredNode.knowledgeObj.title;
        tooltipDate.innerText = hoveredNode.knowledgeObj.date;
        const tags = hoveredNode.knowledgeObj.tags || [];
        tooltipTags.innerText = tags.length ? `[${tags.join(', ')}]` : '';
        tooltip.style.opacity = '1';
    } else {
        hideTooltip();
    }

    // Legend active class update
    document.querySelectorAll('.legend-item').forEach(el => el.classList.remove('active'));
    if (hoveredNode && hoveredNode.lobe && hoveredNode.lobe !== 'stem') {
        const legEl = document.getElementById(`leg-${hoveredNode.lobe}`);
        if (legEl) legEl.classList.add('active');
    }

    // Colors and pulsing logic
    logicNodes.forEach((node, i) => {
        node.pulseTimer += node.pulseSpeed;
        node.activePulse = node.isPulsing ? (Math.sin(node.pulseTimer) + 1) / 2 : 0;

        let targetColor = node.isProject ? PROJECT_DEFAULT_COLOR : DEFAULT_COLOR;
        let targetAlphaMult = 1.0;

        if (hoveredNode) {
            if (node === hoveredNode) {
                targetColor = node.highlightColor;
                targetAlphaMult = 2.5;
            } else if (node.lobe === hoveredNode.lobe && !isMemoryActive) {
                targetColor = node.highlightColor;
                targetAlphaMult = 1.0;
            } else if (node.isProject) {
                targetAlphaMult = 0.3;
            } else {
                targetAlphaMult = 0.1;
            }
        } else if (isMemoryActive && selectedNode) {
            if (node === selectedNode) {
                targetColor = node.highlightColor;
                targetAlphaMult = 2.5;
            } else {
                targetAlphaMult = 0.04;
            }
        }

        node.currentColor.r += (targetColor.r - node.currentColor.r) * 0.1;
        node.currentColor.g += (targetColor.g - node.currentColor.g) * 0.1;
        node.currentColor.b += (targetColor.b - node.currentColor.b) * 0.1;
        node.currentAlphaMult += (targetAlphaMult - node.currentAlphaMult) * 0.1;

        let baseDepthAlpha = 0.1 + 0.9 * Math.max(0, Math.min(1, (node.origZ + 240) / 480));
        let finalAlpha = baseDepthAlpha * node.currentAlphaMult;

        ptCol[i * 4] = node.currentColor.r / 255;
        ptCol[i * 4 + 1] = node.currentColor.g / 255;
        ptCol[i * 4 + 2] = node.currentColor.b / 255;
        ptCol[i * 4 + 3] = node.isProject ? Math.min(1, finalAlpha + 0.3) : (finalAlpha * (0.3 + node.activePulse * 0.7));

        const activeScale = (node === selectedNode && isMemoryActive) ? 1.4 : (node === hoveredNode ? 1.25 : 1.0);
        ptSize[i] = node.baseRadius * activeScale + (node.isProject ? 0 : node.activePulse * 4.0);
    });

    logicEdges.forEach((edge, i) => {
        let alphaMult = Math.min(edge.a.currentAlphaMult, edge.b.currentAlphaMult);
        let finalAlpha = 0.05 * alphaMult;

        if (edge.type === 'obsidian') {
            finalAlpha = 0.4 * alphaMult;
            if (edge.a === hoveredNode || edge.b === hoveredNode) {
                finalAlpha = 1.0;
            }
        }

        const r = edge.a.currentColor.r / 255;
        const g = edge.a.currentColor.g / 255;
        const b = edge.a.currentColor.b / 255;

        lineCol[i * 8] = r; lineCol[i * 8 + 1] = g; lineCol[i * 8 + 2] = b; lineCol[i * 8 + 3] = finalAlpha;
        lineCol[i * 8 + 4] = r; lineCol[i * 8 + 5] = g; lineCol[i * 8 + 6] = b; lineCol[i * 8 + 7] = finalAlpha;
    });

    ptGeo.attributes.aColor.needsUpdate = true;
    ptGeo.attributes.aSize.needsUpdate = true;
    lineGeo.attributes.aColor.needsUpdate = true;

    renderer.render(scene, camera);
}

window.addEventListener('DOMContentLoaded', () => {
    animate();
});