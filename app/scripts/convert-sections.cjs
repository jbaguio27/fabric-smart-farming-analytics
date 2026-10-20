const fs = require('fs');
const path = require('path');

const srcHtmlPath = path.resolve(__dirname, '../../site/index.html');
const outSectionsPath = path.resolve(__dirname, '../src/components/OriginalSections.jsx');
const outFooterPath = path.resolve(__dirname, '../src/components/OriginalFooter.jsx');

const htmlContent = fs.readFileSync(srcHtmlPath, 'utf8');
const lines = htmlContent.split('\n');

function cleanHtmlToJsx(raw) {
  // 1. Comments
  raw = raw.replace(/<!--([\s\S]*?)-->/g, (match, p1) => `{/*${p1}*/}`);

  // 2. Replace failure-matrix with 3D Modern Carousel component
  raw = raw.replace(
    /{\/\* 4 Physical Failure Modes Matrix \(Anti-Slop Clean Engineering Layout\) \*\/}\s*<div class="failure-matrix"[\s\S]*?<\/article>\s*<\/div>/,
    `{/* 4 Physical Failure Modes 3D Modern Carousel */}
        <PhysicalProblemCarousel />`
  );

  // 3. Fix mock-terminal python code multiline & indentation
  const pythonCodeJsx = `<div className="terminal-code-body">
            <pre><code>
<span className="syn-comm"># Verbatim code excerpt from the simulator engine</span>{\`\\n\`}
<span className="syn-kw">class</span> <span className="syn-cls">EnvironmentalTelemetryGenerator</span>(<span className="syn-cls">BaseTelemetryGenerator</span>):{\`\\n\`}
{'    '}<span className="syn-str">&quot;&quot;&quot;Generates continuous microclimate readings for vertical growing zones.&quot;&quot;&quot;</span>{\`\\n\`}
{\`\\n\`}
{'    '}<span className="syn-kw">def</span> <span className="syn-fn">generate_event</span>(<span className="syn-self">self</span>) -&gt; <span className="syn-cls">EnvironmentalTelemetryEvent</span>:{\`\\n\`}
{'        '}facility = <span className="syn-self">self</span>.random_manager.choice(<span className="syn-self">self</span>.settings.facilities){\`\\n\`}
{'        '}zone = <span className="syn-self">self</span>.random_manager.choice(facility.zones){\`\\n\`}
{\`\\n\`}
{'        '}<span className="syn-comm"># Calculate diurnal solar cycle &amp; HVAC thermal response</span>{\`\\n\`}
{'        '}ambient_temp = <span className="syn-self">self</span>.environment_manager.get_zone_temperature(facility.id, zone.id){\`\\n\`}
{'        '}relative_humidity = <span className="syn-self">self</span>.environment_manager.get_zone_humidity(facility.id, zone.id){\`\\n\`}
{'        '}co2_ppm = <span className="syn-self">self</span>.environment_manager.get_zone_co2(facility.id, zone.id){\`\\n\`}
{\`\\n\`}
{'        '}<span className="syn-comm"># Intentional anomaly injection for testing Fabric Activator alerts</span>{\`\\n\`}
{'        '}<span className="syn-kw">if</span> <span className="syn-self">self</span>.settings.enable_ingestion_anomalies <span className="syn-kw">and</span> <span className="syn-self">self</span>.random_manager.random() &lt; <span className="syn-num">0.02</span>:{\`\\n\`}
{'            '}ambient_temp += <span className="syn-self">self</span>.random_manager.uniform(<span className="syn-num">8.5</span>, <span className="syn-num">14.0</span>)  <span className="syn-comm"># Thermal runaway spike</span>{\`\\n\`}
{\`\\n\`}
{'        '}<span className="syn-kw">return</span> <span className="syn-cls">EnvironmentalTelemetryEvent</span>({\`\\n\`}
{'            '}event_type=EVENT_TYPE_ENVIRONMENTAL,{\`\\n\`}
{'            '}facility_id=facility.id,{\`\\n\`}
{'            '}zone_id=zone.id,{\`\\n\`}
{'            '}sensor_type=<span className="syn-str">&quot;ambient_temperature&quot;</span>,{\`\\n\`}
{'            '}sensor_value=round(ambient_temp, <span className="syn-num">2</span>),{\`\\n\`}
{'            '}unit=<span className="syn-str">&quot;celsius&quot;</span>,{\`\\n\`}
{'            '}sensor_status=SENSOR_STATUS_HEALTHY <span className="syn-kw">if</span> ambient_temp &lt; <span className="syn-num">32.0</span> <span className="syn-kw">else</span> SENSOR_STATUS_WARNING,{\`\\n\`}
{'            '}is_daytime=<span className="syn-self">self</span>.environment_manager.is_daytime(),{\`\\n\`}
{'        '})
            </code></pre>
          </div>`;

  raw = raw.replace(
    /<div class="terminal-code-body">[\s\S]*?<\/div>/,
    pythonCodeJsx
  );

  // 4. Fix raw json stream multiline & indentation
  const rawJsonJsx = `<pre className="raw-json-stream"><code>{\`{
  "timestamp": "2026-09-25T00:14:02.184Z",
  "facility_id": "FAC-BGT-01",
  "zone_id": null,  \`}<span className="json-err">&lt;-- MISSING PRIMARY KEY</span>{\`
  "payload": {
    "raw_analog_mv": 892.4,
    "temperature_c": 34.82, \`}<span className="json-warn">&lt;-- THERMAL RUNAWAY SPIKE</span>{\`
    "humidity_pct": 78.4,
    "clock_skew_sec": +420.0,
    "crc_checksum": "ERR_MISMATCH_0x4F"
  },
  "ingestion_status": "QUARANTINED_TO_DLQ",
  "auto_remediation": "WORKER_02_PRIMARY_KEY_LOOKUP"
}
{
  "timestamp": "2026-09-25T00:14:02.392Z",
  "facility_id": "FAC-TAG-02",
  "zone_id": "ZONE-04",
  "payload": {
    "ph_val": 5.48, \`}<span className="json-warn">&lt;-- NUTRIENT LOCKOUT DRIFT</span>{\`
    "ec_val": "2.65mS", \`}<span className="json-err">&lt;-- UNPARSED STRING TYPE</span>{\`
    "pump_vibration_mms": 7.82 \`}<span className="json-warn">&lt;-- CAVITATION SPIKE</span>{\`
  }
}\`}</code></pre>`;

  raw = raw.replace(
    /<pre class="raw-json-stream"><code>[\s\S]*?<\/code><\/pre>/,
    rawJsonJsx
  );

  // 5. class -> className, for -> htmlFor
  raw = raw.replace(/\bclass="/g, 'className="');
  raw = raw.replace(/\bfor="/g, 'htmlFor="');

  // 6. SVG camelCase attributes
  const svgAttrMap = {
    'stroke-width': 'strokeWidth',
    'stroke-linecap': 'strokeLinecap',
    'stroke-linejoin': 'strokeLinejoin',
    'stroke-dasharray': 'strokeDasharray',
    'text-anchor': 'textAnchor',
    'font-size': 'fontSize',
    'font-family': 'fontFamily',
    'stop-color': 'stopColor',
    'stop-opacity': 'stopOpacity',
    'fill-rule': 'fillRule',
    'clip-rule': 'clipRule',
  };

  for (const [k, v] of Object.entries(svgAttrMap)) {
    const reg = new RegExp(`\\b${k}="`, 'g');
    raw = raw.replace(reg, `${v}="`);
  }

  // 7. Void elements self-closing ONLY for standard HTML void elements: img, br, hr, input
  raw = raw.replace(/<img\b([^>]*?)(?<!\/)>/g, '<img$1 />');
  raw = raw.replace(/<br\s*(?<!\/)>/g, '<br />');
  raw = raw.replace(/<hr\s*(?<!\/)>/g, '<hr />');
  raw = raw.replace(/<input\b([^>]*?)(?<!\/)>/g, '<input$1 />');

  // React property names for video
  raw = raw.replace(/\bautoplay\b/g, 'autoPlay');
  raw = raw.replace(/\bplaysinline\b/g, 'playsInline');
  raw = raw.replace(/id="lightbox-img" className="lightbox-img" src=""/g, 'id="lightbox-img" className="lightbox-img"');

  // 8. Unique inline styles
  raw = raw.replace(
    /style="margin: 0\.5rem 0 0\.75rem 1\.5rem; color: var\(--text-secondary\); font-size: 0\.95rem; line-height: 1\.6;"/g,
    'style={{ margin: "0.5rem 0 0.75rem 1.5rem", color: "var(--text-secondary)", fontSize: "0.95rem", lineHeight: "1.6" }}'
  );

  return raw;
}

// Lines 443 to 2113 (0-indexed: 442 to 2113): Main sections
const sectionsRaw = lines.slice(442, 2113).join('\n');
const sectionsJsx = cleanHtmlToJsx(sectionsRaw);

const sectionsComponent = `import React from 'react';
import PhysicalProblemCarousel from './PhysicalProblemCarousel';

export default function OriginalSections() {
  return (
    <>
${sectionsJsx}
    </>
  );
}
`;

fs.writeFileSync(outSectionsPath, sectionsComponent, 'utf8');
console.log('Successfully generated OriginalSections.jsx');

// Lines 2116 to 2160 (0-indexed: 2115 to 2160): Footer and Lightbox modal
const footerRaw = lines.slice(2115, 2160).join('\n');
const footerJsx = cleanHtmlToJsx(footerRaw);

const footerComponent = `import React from 'react';

export default function OriginalFooter() {
  return (
    <>
${footerJsx}
    </>
  );
}
`;

fs.writeFileSync(outFooterPath, footerComponent, 'utf8');
console.log('Successfully generated OriginalFooter.jsx');
