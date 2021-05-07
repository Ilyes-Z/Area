import getUser from "services/user/getUser";

function hasRoles(roles) {
  const userRoles = getUser().roles;

  return roles.every(role => userRoles.includes(role));
}

export default hasRoles;