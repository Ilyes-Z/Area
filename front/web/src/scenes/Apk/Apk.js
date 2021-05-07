import { Button, Container, makeStyles } from '@material-ui/core';
import React from 'react';

const useStyles = makeStyles(theme => ({
  link: {
    textDecoration: 'none',
  },
  button: {
    fontWeight: 'bold',
  }
}))

function Apk() {

  const classes = useStyles();

  return (
    <Container component='main' maxWidth='md'>
    <h1>Apk</h1>

    <a className={classes.link} href="apk/area.apk" download>
      <Button className={classes.button} variant='contained' color='secondary'>Download APK</Button>
    </a>
    </Container>
  );
}

export default Apk;