import { AppBar, Box, Button, IconButton, makeStyles, Toolbar, Typography } from '@material-ui/core';
import { Link, useHistory } from 'react-router-dom';
import { getPath } from 'routes';

import MenuIcon from '@material-ui/icons/Menu';
import ExitToAppIcon from '@material-ui/icons/ExitToApp';
import isAuth from 'services/security/isAuth';

const useStyles = makeStyles((theme) => ({
  title: {
    flexGrow: 1,
    fontWeight: 'bold',
    fontStyle: 'italic',
    textDecoration: 'none',
    color: '#000000',
  },
  link: {
    fontWeight: 'bold',
    margin: '5px',
  },
}));

function Header() {

  const history = useHistory();

  const classes = useStyles();

  return (
    <AppBar position='static'>
      <Toolbar>
        <Box display='flex' flexGrow={1}>
          {/* <IconButton edge='start' color='secondary' aria-label='menu'>
            <MenuIcon />
          </IconButton> */}
          <Typography variant="h5">
            <Link to='/' className={classes.title}>Area</Link>
          </Typography>
        </Box>
        {isAuth() ? (
          <>
            <Button
              onClick={() => history.push(getPath('dashboard'))}
              className={classes.link}
            >
              Dashboard
            </Button>
            <Button
              onClick={() => history.push(getPath('areas'))}
              className={classes.link}
            >
              Areas
            </Button>
            <Button
              onClick={() => history.push(getPath('services'))}
              className={classes.link}
            >
              Services
            </Button>
            <Button
              onClick={() => history.push(getPath('apk'))}
              className={classes.link}
            >
              Apk
            </Button>
            <IconButton
              onClick={() => {
                localStorage.removeItem('user');
                window.location.reload();
              }}
              color='secondary'
            >
              <ExitToAppIcon />
            </IconButton>
          </>
        ) : (
          <>
            <Button
              onClick={() => history.push(getPath('apk'))}
              className={classes.link}
            >
              Apk
            </Button>
            <Button
              onClick={() => history.push(getPath('login'))}
              variant='contained'
              color='secondary'
              className={classes.link}
            >
              Sign in
            </Button>
            <Button
              onClick={() => history.push(getPath('register'))}
              variant='outlined'
              className={classes.link}
            >
              Sign up
            </Button>
          </>
        )}
      </Toolbar>
    </AppBar>
  );
}

export default Header;