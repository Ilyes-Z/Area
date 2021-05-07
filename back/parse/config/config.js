module.exports = {
    emailAdapter: {
        module: "parse-smtp-template",
        options: {
            port: 25,
            host: 'smtpserver',
            user: '',
            password: '',
            fromAddress: 'noreply@area-revenge.ninja',
            template: true,
            templatePath: "/views/email/templates/template.html"
        }
    }
}