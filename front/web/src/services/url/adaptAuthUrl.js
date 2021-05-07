function adaptAuthUrl(url) {
    return url.replace('<hostname>',
        process.env.REACT_APP_AREA_HOST === 'localhost' ? 'http://localhost:8080/' : 'https://api.area-revenge.ninja/');
}

export default adaptAuthUrl;