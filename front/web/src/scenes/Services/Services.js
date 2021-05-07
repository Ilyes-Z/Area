import { useEffect, useState} from 'react';
import { Button, Container, Grid, Paper, makeStyles } from '@material-ui/core';
import getUser from 'services/user/getUser';
import API from 'api';
import adaptAuthUrl from 'services/url/adaptAuthUrl';


const useStyles = makeStyles(theme => ({
  paper: {
    padding: theme.spacing(2),
  },
}))

function Services() {
  const [services, setServices] = useState([]);

  const sessionToken = getUser().sessionToken;

  const classes = useStyles();

  useEffect(() => {
    API.get('/services?auth=true', {
      headers: {
        'Authorization': `Bearer ${sessionToken}`,
      }
    }).then(response => {
      setServices(response.data.results);
    }).catch(response => {
      console.log(response);
    })
  }, []);

  const openAuthWindow = (url) => {
    const newWindow = window.open(url, '_blank', 'toolbar=0,status=0,width=600,height=850');

    var timer = setInterval(() => {
      if (newWindow.closed) {
        window.location.reload();
        clearInterval(timer);
      }
    }, 1000);
  }

  const disconnectService = (name) => {
    API.delete(`/service/${name}`, {
      headers: {
        'Authorization': `Bearer ${sessionToken}`,
      }
    }).then(response => {
      console.log(response);
      window.location.reload();
    }).catch(error => {
      console.log(error);
    })
  }

  return (
    <Container component='main' maxWidth='md'>
      <h1>Services</h1>
      <Grid container justify='center' spacing={2}>
        {services.map((service, key) => {
          if (!service.auth_required || !service.auth_parameter.url) return;

          const url = adaptAuthUrl(service.auth_parameter.url).replace('<session_token>', sessionToken);

          return (
            <Grid item xs={6} key={key}>
              <Paper className={classes.paper} elevation={3}>
                <h2>{service.name}</h2>
                {service.connected ? (
                  <Button variant='contained' color='secondary' onClick={() => disconnectService(service.name)}>Disconnect</Button>
                ) : (
                  <Button variant='contained' color='secondary' onClick={() => openAuthWindow(url)}>connect to {service.name}</Button>
                )}
              </Paper>
            </Grid>
          );
        })}
      </Grid>
    </Container>
  );
}

export default Services;