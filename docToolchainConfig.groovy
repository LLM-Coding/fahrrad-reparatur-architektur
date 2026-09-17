// docToolchain v4 configuration for the keynote project.
// Based on template_config/Config.groovy of docToolchain 4.0.0 (branch main-4.x).

outputPath = 'build'

// Path where docToolchain searches for input files, relative to the project root.
inputPath = 'src/docs'

// Custom Asciidoctor extensions (Ruby), relative to the project root.
// rubyExtensions = []

inputFiles = [
    [file: 'arc42/arc42.adoc', formats: ['html', 'pdf']],
    /** inputFiles **/
]

// Folders in which Asciidoctor finds images, relative to inputPath.
// They are copied as resources to ./images. Use ifndef::imagesdir[...] in documents.
imageDirs = [
    'images',
    /** imageDirs **/
]

// Task-level options
taskInputsDirs = [
    "${inputPath}",
]
taskInputsFiles = []

//******************************************************************************
// Microsite: generateSite + previewSite
// microsite.foo becomes site.foo in jBake (config.site_foo in templates).
microsite = [:]
microsite.with {
    /** start:microsite **/
    contextPath = '/'
    /** end:microsite **/
    title = 'Fahrrad-Reparatur-System: Architektur und ADRs'
    siteTitle = 'Wir bauen eine Software-Architektur \u2013 ADRs'
    // Landing page, relative to inputPath (src/docs). Static HTML fragment, no JS.
    landingPage = 'landingpage.gsp'
    // Menu: code -> title. Codes come from :jbake-menu: headers or folder names.
    menu = [arc42: 'arc42']
    footerMail = ''
    footerTwitter = ''
    footerSO = ''
    footerGithub = ''
    footerSlack = ''
    footerText = '<small class="text-white">built with <a href="https://doctoolchain.org">docToolchain</a> &middot; powered by <a href="https://asciidoctor.org">AsciiDoctor</a></small>'
    footerLogo = ''
    logo = ''
    branch = System.getenv("DTC_PROJECT_BRANCH") ?: '-'
}
