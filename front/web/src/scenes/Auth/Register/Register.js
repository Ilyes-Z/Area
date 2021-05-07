import React, { useState } from 'react';
import { Link, useHistory } from 'react-router-dom';
import { makeStyles } from '@material-ui/core/styles';
import { Avatar, Button, CssBaseline, TextField, Grid, Typography, Container, Paper } from '@material-ui/core'

import { getPath } from 'routes';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import API from 'api';


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
  link: {
    color: '#000000',
    fontWeight: 'bold',
  }
}));

export default function Register() {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirmation, setPasswordConfirmation] = useState('');

  const history = useHistory();

  const classes = useStyles();

  const handleEmail = (e) => setEmail(e.target.value);
  const handleUsername = (e) => setUsername(e.target.value);
  const handlePassword = (e) => setPassword(e.target.value);
  const handlePasswordConfirmation = (e) => setPasswordConfirmation(e.target.value);

  function onSubmit(event) {
    event.preventDefault();

    if (password !== passwordConfirmation) {
      console.log('No match beetween passwords, try again !');
      return;
    }

    API.post('/auth/register', {
      email: email, username: username, password: password
    }).then(response => {
      history.push(getPath('login'));
    }).catch(response => {
      console.log(response);
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
          Sign up !
        </Typography>
        <form className={classes.form} noValidate onSubmit={onSubmit}>
          <TextField
            variant="outlined"
            color='secondary'
            margin="normal"
            required
            fullWidth
            id="username"
            label="Username "
            name="username"
            value={username}
            onChange={handleUsername}
            autoFocus
          />
          <TextField
            variant="outlined"
            color='secondary'
            margin="normal"
            required
            fullWidth
            id="email"
            label="Email"
            name="email"
            value={email}
            onChange={handleEmail}
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
          <TextField
            variant="outlined"
            color='secondary'
            margin="normal"
            required
            fullWidth
            name="confirm-password"
            label="Confirm password"
            type="password"
            id="confirm-password"
            value={passwordConfirmation}
            onChange={handlePasswordConfirmation}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="secondary"
            className={classes.submit}
          >
            Sign up
          </Button>
          <Grid container>
            <Grid item>
              {"Already on Area ? "}
              <Link className={classes.link} to="/auth/login">
                {"Sign in"}
              </Link>
            </Grid>
          </Grid>
        </form>
      </Paper>
    </Container>
  );
}