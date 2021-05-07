import { Container, makeStyles, Typography } from '@material-ui/core';
import React from 'react';

import logo from './logo.png'

const useStyles = makeStyles(theme => ({
  title: {
    marginTop:theme.spacing(5),
    fontWeight: 'bold',
    textAlign: 'center'
  },
  logo: {
    marginTop:theme.spacing(10),
    display: 'block',
    marginLeft: 'auto',
    marginRight: 'auto',
    width: '25%',
    height: 'auto',
  },
  subtitle: {
    marginTop:theme.spacing(2),
    fontWeight: 'bold',
    textAlign: 'center'
  },
}));

function Home() {

  const classes = useStyles();

  return (
    <Container component='main' maxWidth='md'>
      <a href="https://youtu.be/haW20SpUEl8?t=54" target="_blank" rel="noopener noreferrer">
        <img className={classes.logo} src={logo} alt='logo' />
      </a>
      <Typography className={classes.title} component='h1' variant='h4'>
        AREA-REVENGE
      </Typography>
      <Typography className={classes.subtitle} component="h3" variant="h6">
        Action-reaction service
      </Typography>
    </Container>
  );
}

export default Home;