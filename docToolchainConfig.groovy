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
// Microsite: generateSite + previewSite (disabled until a site theme is chosen)
//
// microsite = [:]
// microsite.with {
//     /** start:microsite **/
//     contextPath = '/'
//     siteFolder = '../site'
//     /** end:microsite **/
//     title = 'Keynote'
//     footerMail = ''
//     footerTwitter = ''
//     footerSO = ''
//     footerGithub = ''
//     footerSlack = ''
//     menu = [:]
//     landingPage = 'landingpage.gsp'
//     footerText = ''
//     footerLogo = ''
//     logo = ''
// }
