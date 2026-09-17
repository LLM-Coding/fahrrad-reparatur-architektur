<div class="row flex-xl-nowrap">
    <main class="col-12 col-md-12 col-xl-12 pl-md-12" role="main">

        <!-- Hero -->
        <section class="row align-items-center py-4 mb-4">
            <div class="col-lg-6 mb-4 mb-lg-0">
                <h1 class="display-4">Wir bauen eine Software-Architektur</h1>
                <p class="lead">
                    Architekturdokumentation und ADRs zu Eberhard Wolffs Architektur-Kata
                    Fahrrad-Reparatur-System, software-architektur.tv Folgen 111 bis 113.
                </p>
                <p>
                    <a class="btn btn-primary btn-lg mr-2 mb-2" href="arc42/chapters/09_architecture_decisions.html">Zu den Entscheidungen</a>
                    <a class="btn btn-outline-secondary btn-lg mb-2" href="arc42/chapters/01_introduction_and_goals.html">Einf&uuml;hrung</a>
                </p>
            </div>
            <div class="col-lg-6 text-center">
                <!-- Hero-Bild: sobald images/landingpage-hero.png existiert, hier einbinden.
                     Bis dahin zeigt die Seite die Entscheidungslandkarte aus Kapitel 9. -->
                <a href="arc42/chapters/09_architecture_decisions.html" title="Entscheidungslandkarte, Kapitel 9">
                    <img src="images/09-entscheidungslandkarte.svg" alt="Entscheidungslandkarte der Architekturentscheidungen" class="img-fluid rounded border">
                </a>
                <p class="small text-muted mt-2 mb-0">
                    <span style="display:inline-block;width:.9em;height:.9em;background:#c8e6c9;border:1px solid #2e7d32;vertical-align:middle"></span> gefallen &nbsp;
                    <span style="display:inline-block;width:.9em;height:.9em;background:#fff59d;border:1px solid #f9a825;vertical-align:middle"></span> vertagt &nbsp;
                    <span style="display:inline-block;width:.9em;height:.9em;background:#ffcdd2;border:1px solid #c62828;vertical-align:middle"></span> offen
                </p>
            </div>
        </section>

        <!-- Kacheln -->
        <section class="row">

            <div class="col-md-4 mb-4">
                <div class="card h-100 shadow-sm">
                    <div class="card-body">
                        <!-- Icon: einfuehrung -->
                        <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="text-primary mb-2" viewBox="0 0 16 16"><path d="M8 16.016a7.5 7.5 0 0 0 1.962-14.74A1 1 0 0 0 9 0H7a1 1 0 0 0-.962 1.276A7.5 7.5 0 0 0 8 16.016m6.5-7.5a6.5 6.5 0 1 1-13 0 6.5 6.5 0 0 1 13 0"/><path d="m6.94 7.44 4.95-2.83-2.83 4.95-4.949 2.83 2.828-4.95z"/></svg>
                        <h2 class="h5 card-title">Einf&uuml;hrung und Ziele</h2>
                        <p class="card-text">Was das Fahrrad-Reparatur-System leisten soll und welche Qualit&auml;tsziele die Architektur pr&auml;gen.</p>
                        <a href="arc42/chapters/01_introduction_and_goals.html" class="stretched-link">Kapitel 1</a>
                    </div>
                </div>
            </div>

            <div class="col-md-4 mb-4">
                <div class="card h-100 shadow-sm">
                    <div class="card-body">
                        <!-- Icon: kontext -->
                        <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="text-primary mb-2" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M6 3.5A1.5 1.5 0 0 1 7.5 2h1A1.5 1.5 0 0 1 10 3.5v1A1.5 1.5 0 0 1 8.5 6v1H14a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-1 0V8h-5v.5a.5.5 0 0 1-1 0V8h-5v.5a.5.5 0 0 1-1 0v-1A.5.5 0 0 1 2 7h5.5V6A1.5 1.5 0 0 1 6 4.5zM8.5 5a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1a.5.5 0 0 0 .5.5zM0 11.5A1.5 1.5 0 0 1 1.5 10h1A1.5 1.5 0 0 1 4 11.5v1A1.5 1.5 0 0 1 2.5 14h-1A1.5 1.5 0 0 1 0 12.5zm1.5-.5a.5.5 0 0 0-.5.5v1a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5zm4.5.5A1.5 1.5 0 0 1 7.5 10h1a1.5 1.5 0 0 1 1.5 1.5v1A1.5 1.5 0 0 1 8.5 14h-1A1.5 1.5 0 0 1 6 12.5zm1.5-.5a.5.5 0 0 0-.5.5v1a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5zm4.5.5a1.5 1.5 0 0 1 1.5-1.5h1a1.5 1.5 0 0 1 1.5 1.5v1a1.5 1.5 0 0 1-1.5 1.5h-1a1.5 1.5 0 0 1-1.5-1.5zm1.5-.5a.5.5 0 0 0-.5.5v1a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5z"/></svg>
                        <h2 class="h5 card-title">Kontext</h2>
                        <p class="card-text">Wer mit dem System arbeitet und welche Nachbarsysteme es anbindet: Webshop, Kasse, Zahlungsdienst, Rechnungswesen.</p>
                        <a href="arc42/chapters/03_context_and_scope.html" class="stretched-link">Kapitel 3</a>
                    </div>
                </div>
            </div>

            <div class="col-md-4 mb-4">
                <div class="card h-100 shadow-sm">
                    <div class="card-body">
                        <!-- Icon: bausteine -->
                        <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="text-primary mb-2" viewBox="0 0 16 16"><path d="M7.752.066a.5.5 0 0 1 .496 0l3.75 2.143a.5.5 0 0 1 .252.434v3.995l3.498 2A.5.5 0 0 1 16 9.07v4.286a.5.5 0 0 1-.252.434l-3.75 2.143a.5.5 0 0 1-.496 0l-3.502-2-3.502 2.001a.5.5 0 0 1-.496 0l-3.75-2.143A.5.5 0 0 1 0 13.357V9.071a.5.5 0 0 1 .252-.434L3.75 6.638V2.643a.5.5 0 0 1 .252-.434zM4.25 7.504 1.508 9.071l2.742 1.567 2.742-1.567zM7.5 9.933l-2.75 1.571v3.134l2.75-1.571zm1 3.134 2.75 1.571v-3.134L8.5 9.933zm.508-3.996 2.742 1.567 2.742-1.567-2.742-1.567zm2.242-2.433V3.504L8.5 5.076V8.21zM7.5 8.21V5.076L4.75 3.504v3.134zM5.258 2.643 8 4.21l2.742-1.567L8 1.076zM15 9.933l-2.75 1.571v3.134L15 13.067zM3.75 14.638v-3.134L1 9.933v3.134z"/></svg>
                        <h2 class="h5 card-title">Bausteine</h2>
                        <p class="card-text">Wie das System in Module zerf&auml;llt und welche Verantwortung jeder Baustein tr&auml;gt.</p>
                        <a href="arc42/chapters/05_building_block_view.html" class="stretched-link">Kapitel 5</a>
                    </div>
                </div>
            </div>

            <div class="col-md-4 mb-4">
                <div class="card h-100 shadow-sm">
                    <div class="card-body">
                        <!-- Icon: entscheidungen -->
                        <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="text-primary mb-2" viewBox="0 0 16 16"><path d="M7 7V1.414a1 1 0 0 1 2 0V2h5a1 1 0 0 1 .8.4l.975 1.3a.5.5 0 0 1 0 .6L14.8 5.6a1 1 0 0 1-.8.4H9v10H7v-5H2a1 1 0 0 1-.8-.4L.225 9.3a.5.5 0 0 1 0-.6L1.2 7.4A1 1 0 0 1 2 7zm1 3V8H2l-.75 1L2 10zm0-5h6l.75-1L14 3H8z"/></svg>
                        <h2 class="h5 card-title">Entscheidungen</h2>
                        <p class="card-text">Die ADRs aus den drei Folgen: welche Optionen zur Wahl standen und warum eine gewonnen hat.</p>
                        <a href="arc42/chapters/09_architecture_decisions.html" class="stretched-link">Kapitel 9</a>
                    </div>
                </div>
            </div>

            <div class="col-md-4 mb-4">
                <div class="card h-100 shadow-sm">
                    <div class="card-body">
                        <!-- Icon: qualitaet -->
                        <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="text-primary mb-2" viewBox="0 0 16 16"><path d="M8 4a.5.5 0 0 1 .5.5V6a.5.5 0 0 1-1 0V4.5A.5.5 0 0 1 8 4M3.732 5.732a.5.5 0 0 1 .707 0l.915.914a.5.5 0 1 1-.708.708l-.914-.915a.5.5 0 0 1 0-.707M2 10a.5.5 0 0 1 .5-.5h1.586a.5.5 0 0 1 0 1H2.5A.5.5 0 0 1 2 10m9.5 0a.5.5 0 0 1 .5-.5h1.5a.5.5 0 0 1 0 1H12a.5.5 0 0 1-.5-.5m.754-4.246a.39.39 0 0 0-.527-.02L7.547 9.31a.91.91 0 1 0 1.302 1.258l3.434-4.297a.39.39 0 0 0-.029-.518z"/><path fill-rule="evenodd" d="M0 10a8 8 0 1 1 15.547 2.661c-.442 1.253-1.845 1.602-2.932 1.25C11.309 13.488 9.475 13 8 13c-1.474 0-3.31.488-4.615.911-1.087.352-2.49.003-2.932-1.25A8 8 0 0 1 0 10m8-7a7 7 0 0 0-6.603 9.329c.203.575.923.876 1.68.63C4.397 12.533 6.358 12 8 12s3.604.532 4.923.96c.757.245 1.477-.056 1.68-.631A7 7 0 0 0 8 3"/></svg>
                        <h2 class="h5 card-title">Qualit&auml;t</h2>
                        <p class="card-text">Messbare Qualit&auml;tsszenarien f&uuml;r Benutzbarkeit, Zuverl&auml;ssigkeit und &Auml;nderbarkeit, mit Bezug zu den ADRs.</p>
                        <a href="arc42/chapters/10_quality_requirements.html" class="stretched-link">Kapitel 10</a>
                    </div>
                </div>
            </div>

            <div class="col-md-4 mb-4">
                <div class="card h-100 shadow-sm">
                    <div class="card-body">
                        <!-- Icon: risiken -->
                        <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="text-primary mb-2" viewBox="0 0 16 16"><path d="M7.938 2.016A.13.13 0 0 1 8.002 2a.13.13 0 0 1 .063.016.15.15 0 0 1 .054.057l6.857 11.667c.036.06.035.124.002.183a.2.2 0 0 1-.054.06.1.1 0 0 1-.066.017H1.146a.1.1 0 0 1-.066-.017.2.2 0 0 1-.054-.06.18.18 0 0 1 .002-.183L7.884 2.073a.15.15 0 0 1 .054-.057m1.044-.45a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767z"/><path d="M7.002 12a1 1 0 1 1 2 0 1 1 0 0 1-2 0M7.1 5.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0z"/></svg>
                        <h2 class="h5 card-title">Risiken</h2>
                        <p class="card-text">Offene Risiken und technische Schulden, priorisiert nach Wahrscheinlichkeit und Auswirkung.</p>
                        <a href="arc42/chapters/11_technical_risks.html" class="stretched-link">Kapitel 11</a>
                    </div>
                </div>
            </div>

        </section>

        <!-- Quellen -->
        <footer class="border-top pt-3 mt-2 small text-muted">
            <p class="mb-1"><strong>Quellen:</strong>
                software-architektur.tv
                <a href="https://software-architektur.tv/2022/02/25/folge111.html">Folge 111</a>,
                <a href="https://software-architektur.tv/2022/03/11/folge112.html">Folge 112</a>,
                <a href="https://software-architektur.tv/2022/03/25/folge113.html">Folge 113</a>
                sowie das Repository
                <a href="https://github.com/LLM-Coding/fahrrad-reparatur-architektur">LLM-Coding/fahrrad-reparatur-architektur</a>.
            </p>
            <p class="mb-0">Icons: <a href="https://icons.getbootstrap.com/">Bootstrap Icons</a> (MIT).</p>
        </footer>

    </main>
</div>
