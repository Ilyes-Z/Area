import { Container, makeStyles, Paper, Typography, Button } from "@material-ui/core";
import { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';

import Action from 'components/Action/Action';
import API from 'api';
import getUser from "services/user/getUser";
import { getPath } from "routes";

const useStyles = makeStyles(theme => ({
  title: {
    marginTop: theme.spacing(5),
    fontWeight: "bold",
    textAlign: "center"
  },
  trigger: {
    marginTop: theme.spacing(5),
    alignItems: 'center',
    display: 'flex',
    flexDirection: 'column',
    padding: '30px',
    borderRadius: "10px",
  },
  reaction: {
    marginTop: theme.spacing(5),
    marginBottom: theme.spacing(5),
    alignItems: 'center',
    display: 'flex',
    flexDirection: 'column',
    padding: '30px',
    borderRadius: "10px",
  },
  triggerTitle: {
    fontWeight: 'bold',
  },
  triggerDescription: {
  },
}));

function Dashboard() {

  const classes = useStyles();

  const history = useHistory();

  const [services, setServices] = useState([]);

  const [trigger, setTrigger] = useState({ service: null, action: null, parameters: {} });
  const [reaction, setReaction] = useState({ service: null, action: null, parameters: {} });

  const handleTrigger = (trigger) => { setTrigger(trigger); };
  const handleReaction = (reaction) => { setReaction(reaction) };

  const handleSubmit = (event) => {
    event.preventDefault();

    const triggerParam = services.find(s => s.name === trigger.service).triggers.find(t => t.id === trigger.action).parameters;
    const reactionParam = services.find(s => s.name === reaction.service).reactions.find(t => t.id === reaction.action).parameters;

    triggerParam.map(param => {
      if (param.type === 'array') {
        trigger.parameters[param.name] = trigger.parameters[param.name].split(';');
      }
      return;
    })

    reactionParam.map(param => {
      if (param.type === 'array') {
        reaction.parameters[param.name] = reaction.parameters[param.name].split(';');
      }
      return;
    })

    const option = {
      headers: {
        'Authorization': `Bearer ${getUser().sessionToken}`,
        'Content-Type': 'application/json',
      },
    }

    const body = {
      services: {
        trigger: services.find(service => service.name === trigger.service).objectId,
        reaction: services.find(service => service.name === reaction.service).objectId,
      },
      trigger: {
        id: trigger.action,
        ...trigger.parameters
      },
      reaction: {
        id: reaction.action,
        ...reaction.parameters
      }
    }
    API.post('/area/', body, option).then(response => {
      history.push(getPath('areas'));
    }).catch(response => {
      console.log(response);
    })
  };

  useEffect(() => {
    API.get('/services?auth=true').then(response => {
      setServices(response.data.results);
    }).catch(response => {
      console.log(response);
    })
  }, []);

  return (
    <Container component="main" maxWidth="md">
      <Typography className={classes.title} component="h1" variant="h4">
        Welcome to AREA !
      </Typography>
      <form autoComplete="off" onSubmit={handleSubmit}>
        <Paper elevation={3} className={classes.trigger}>
          <Typography className={classes.triggerTitle} component="h2" variant="h5">
            Create your own automated tasks
          </Typography>
          <Typography className={classes.triggerDescription} component="h3" variant="h6">
            You know what you want ? Start by choosing a trigger.
          </Typography>
          <Action type="triggers" services={services} handler={handleTrigger} />
      </Paper>
      {trigger.service && trigger.action ? (
        <>
          <Paper elevation={3} className={classes.reaction}>
            <Action type="reactions" triggerId={trigger.action} services={services} handler={handleReaction} />
          </Paper>
          <Button fullWidth type="submit" variant="contained" color="secondary">Submit</Button>
        </>
      ) : (<></>)}
      </form>
    </Container>
  );
}

export default Dashboard;