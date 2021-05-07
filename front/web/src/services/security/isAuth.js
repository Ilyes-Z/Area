import getUser from "services/user/getUser";

function isAuth() {
  const user = getUser()

  return user && user.sessionToken ? true : false;
}

export default isAuth;