function getUser() {
    return JSON.parse(localStorage.getItem('user'));
}

export default getUser;