import { useState } from 'react';

import { makeStyles } from '@material-ui/core/styles';
import { Avatar, Button, CssBaseline, TextField, Typography, Container, Paper } from '@material-ui/core'

import LockOutlinedIcon from '@material-ui/icons/LockOutlined';

import API from 'api';
import { useHistory } from 'react-router-dom';
import { getPath } from 'routes';

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
}));

function Recuperation() {

  const [email, setEmail] = useState('');

  const classes = useStyles();

  const history = useHistory();

  const handleEmail = (e) => setEmail(e.target.value);

  const onSubmit = (event) => {
    event.preventDefault();

    API.post('/user/email', {
      email: email,
    }).then(response => {
      console.log(response);

      history.push(getPath('login'));
    }).catch(error => {
      console.log(error.response);
    })
  };

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <Paper elevation={3} className={classes.paper}>
        <Avatar className={classes.avatar}>
          <LockOutlinedIcon />
        </Avatar>
        <Typography component="h1" variant="h5">
          Reset your password !
        </Typography>
        <form className={classes.form} noValidate onSubmit={onSubmit}>
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
            autoFocus
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="secondary"
            className={classes.submit}
          >
            Send email
          </Button>
        </form>
      </Paper>
    </Container>
  );
}

export default Recuperation;