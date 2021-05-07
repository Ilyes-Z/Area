import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { makeStyles } from '@material-ui/core/styles';
import { Avatar, Button, CssBaseline, TextField, Grid, Typography, Container, Paper } from '@material-ui/core'

import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import API from 'api';
import { getPath } from 'routes';
import axios from 'axios';

const useStyles = makeStyles(theme => ({
  paper: {
    marginTop: theme.spacing(10),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: '30px'
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: '#000000',
  },
  form: {
    width: '100%',
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
  auth: {
    fontWeight: 'bold',
    margin: theme.spacing(3, 0, 0),
  },
  link: {
    color: '#000000',
    fontWeight: 'bold',
  },
  register: {
    marginTop: theme.spacing(2),
  },
}));

export default function Login({setLogged, ...props}) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const [spotify, setSpotify] = useState({});
  const [github, setGithub] = useState({});

  const classes = useStyles();

  const handleEmail = (e) => setEmail(e.target.value);
  const handlePassword = (e) => setPassword(e.target.value);

  useEffect(() => {
    API.get('/service/spotify').then(response => {
      setSpotify(response.data);
    }).catch(response => {
      console.log(response);
    })

    API.get('/service/github').then(response => {
      setGithub(response.data);
    }).catch(response => {
      console.log(response);
    })
  }, []);

  function onSubmit(event) {
    event.preventDefault();

    const url = `/auth/login?username=${email}&password=${password}`;

    API.get(url).then((response) => {
      localStorage.setItem('user', JSON.stringify({
        username: response.data.username,
        email: response.data.email,
        sessionToken: response.data.sessionToken,
      }));
      window.location.reload();
    }).catch((response) => {
      console.log(response.response);
    })
  }

  const handleServiceAuth = (url) => {
    axios.post(url).then(response => {
      console.log(response);
    }).catch(error => {
      console.log(error.response);
    })
  }

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <Paper elevation={3} className={classes.paper}>
        <Avatar className={classes.avatar}>
          <LockOutlinedIcon />
        </Avatar>
        <Typography component="h1" variant="h5">
          Sign in !
        </Typography>
        <form className={classes.form} noValidate onSubmit={onSubmit}>
          <TextField
            variant="outlined"
            color='secondary'
            margin="normal"
            required
            fullWidth
            id="email"
            label="Username or email address"
            name="email"
            value={email}
            onChange={handleEmail}
            autoFocus
          />
          <TextField
            variant="outlined"
            color='secondary'
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            value={password}
            onChange={handlePassword}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="secondary"
            className={classes.submit}
          >
            Sign in
          </Button>
          <Grid container>
            <Grid item>
              <Link className={classes.link} to={getPath('recuperation')}>
                {"Forgot password ? "}
              </Link>
            </Grid>
          </Grid>
          {/* <Button
            fullWidth
            color="secondary"
            variant="contained"
            className={classes.auth}
          >
            Sign up with Spotify
          </Button>
          <Button
            fullWidth
            color="secondary"
            variant="contained"
            className={classes.auth}
          >
            Sign up with Github
          </Button> */}
        </form>
      </Paper>
      <Grid container justify="center">
        <Grid item className={classes.register}>
          {"New to Area ? "}
          <Link className={classes.link} to={getPath('register')}>
            {"Join now"}
          </Link>
        </Grid>
      </Grid>
    </Container>
  );
}