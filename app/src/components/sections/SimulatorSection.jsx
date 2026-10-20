import React from 'react';

export default function SimulatorSection() {
  return (
    <section id="build" className="section">
      <div className="container">
        <h2 className="section-title">The Synthetic Data Simulator</h2>
        <p className="section-lead">
          Because the real farm's systems were not modernized and could not be used for a public platform, I wrote a modular Python telemetry generator. It simulates 8 vertical farming facilities with 10 distinct growing zones each (80 monitored microclimates), generating the realistic data volumes needed to test a modern architecture.
        </p>

        <div className="build-progression">
          <div className="progression-step">
            <div className="progression-number">Stage 01</div>
            <div className="progression-title">Observed Farm Reality</div>
            <div className="progression-desc">Encountered fragmented operational records, manual whiteboards, isolated equipment logs, and the practical constraints that prevented immediate on-site modernization.</div>
          </div>
          <div className="progression-step">
            <div className="progression-number">Stage 02</div>
            <div className="progression-title">Synthetic Telemetry Simulator</div>
            <div className="progression-desc">Engineered a multi-threaded Python simulator emitting 6 continuous IoT-style channels with deterministic seeds, clock skew, and injected anomalies to model the problem without proprietary data.</div>
          </div>
          <div className="progression-step">
            <div className="progression-number">Stage 03</div>
            <div className="progression-title">Microsoft Fabric Proof of Concept</div>
            <div className="progression-desc">Constructed an end-to-end cloud platform demonstrating how those fragmented sources could be unified through Eventstream, KQL, Delta Medallion Lakehouse, Kimball modeling, and Direct Lake reporting.</div>
          </div>
        </div>

        {/* Modern Developer Mock Terminal Window */}
        <div className="mock-terminal">
          <div className="terminal-topbar">
            <div className="terminal-dots">
              <span className="terminal-dot dot-red"></span>
              <span className="terminal-dot dot-yellow"></span>
              <span className="terminal-dot dot-green"></span>
            </div>
            <div className="terminal-tab-title">
              <span className="terminal-prompt-icon">&gt;_</span>
              <span>src/smart_farming/generators/environmental_telemetry_generator.py</span>
            </div>
            <button className="code-copy-btn">Copy Excerpt</button>
          </div>
          <div className="terminal-code-body">
            <pre><code>
<span className="syn-comm"># Verbatim code excerpt from the simulator engine</span>{`\n`}
<span className="syn-kw">class</span> <span className="syn-cls">EnvironmentalTelemetryGenerator</span>(<span className="syn-cls">BaseTelemetryGenerator</span>):{`\n`}
{'    '}<span className="syn-str">&quot;&quot;&quot;Generates continuous microclimate readings for vertical growing zones.&quot;&quot;&quot;</span>{`\n`}
{`\n`}
{'    '}<span className="syn-kw">def</span> <span className="syn-fn">generate_event</span>(<span className="syn-self">self</span>) -&gt; <span className="syn-cls">EnvironmentalTelemetryEvent</span>:{`\n`}
{'        '}facility = <span className="syn-self">self</span>.random_manager.choice(<span className="syn-self">self</span>.settings.facilities){`\n`}
{'        '}zone = <span className="syn-self">self</span>.random_manager.choice(facility.zones){`\n`}
{`\n`}
{'        '}<span className="syn-comm"># Calculate diurnal solar cycle &amp; HVAC thermal response</span>{`\n`}
{'        '}ambient_temp = <span className="syn-self">self</span>.environment_manager.get_zone_temperature(facility.id, zone.id){`\n`}
{'        '}relative_humidity = <span className="syn-self">self</span>.environment_manager.get_zone_humidity(facility.id, zone.id){`\n`}
{'        '}co2_ppm = <span className="syn-self">self</span>.environment_manager.get_zone_co2(facility.id, zone.id){`\n`}
{`\n`}
{'        '}<span className="syn-comm"># Intentional anomaly injection for testing Fabric Activator alerts</span>{`\n`}
{'        '}<span className="syn-kw">if</span> <span className="syn-self">self</span>.settings.enable_ingestion_anomalies <span className="syn-kw">and</span> <span className="syn-self">self</span>.random_manager.random() &lt; <span className="syn-num">0.02</span>:{`\n`}
{'            '}ambient_temp += <span className="syn-self">self</span>.random_manager.uniform(<span className="syn-num">8.5</span>, <span className="syn-num">14.0</span>)  <span className="syn-comm"># Thermal runaway spike</span>{`\n`}
{`\n`}
{'        '}<span className="syn-kw">return</span> <span className="syn-cls">EnvironmentalTelemetryEvent</span>({`\n`}
{'            '}event_type=EVENT_TYPE_ENVIRONMENTAL,{`\n`}
{'            '}facility_id=facility.id,{`\n`}
{'            '}zone_id=zone.id,{`\n`}
{'            '}sensor_type=<span className="syn-str">&quot;ambient_temperature&quot;</span>,{`\n`}
{'            '}sensor_value=round(ambient_temp, <span className="syn-num">2</span>),{`\n`}
{'            '}unit=<span className="syn-str">&quot;celsius&quot;</span>,{`\n`}
{'            '}sensor_status=SENSOR_STATUS_HEALTHY <span className="syn-kw">if</span> ambient_temp &lt; <span className="syn-num">32.0</span> <span className="syn-kw">else</span> SENSOR_STATUS_WARNING,{`\n`}
{'            '}is_daytime=<span className="syn-self">self</span>.environment_manager.is_daytime(),{`\n`}
{'        '})
            </code></pre>
          </div>
        </div>
      </div>
    </section>
  );
}
