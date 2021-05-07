import { Grid, Paper, Typography, Switch, FormControlLabel, makeStyles, IconButton } from '@material-ui/core';
import { useState } from 'react';

import DeleteIcon from '@material-ui/icons/Delete';

import getUser from 'services/user/getUser';
import API from 'api';
import { getPath } from 'routes';

const switchStyle = makeStyles(theme => ({
  root: {
    width: 42,
    height: 26,
    padding: 0,
  },
  switchBase: {
    padding: 1,
    '&$checked': {
      transform: 'translateX(16px)',
      color: theme.palette.common.white,
      '& + $track': {
        backgroundColor: '#000000',
        opacity: 1,
        border: 'none',
      },
    },
    '&$focusVisible $thumb': {
      color: '#52d869',
      border: '6px solid #fff',
    },
  },
  thumb: {
    width: 24,
    height: 24,
  },
  track: {
    borderRadius: 26 / 2,
    border: `1px solid ${theme.palette.grey[400]}`,
    backgroundColor: theme.palette.grey[50],
    opacity: 1,
    transition: theme.transitions.create(['background-color', 'border']),
  },
  checked: {},
  focusVisible: {},
}));

function AreaItem({area, services, history, ...props}) {

  const [activity, setActivity] = useState(area.is_actif);

  const triggerServiceName = area.trigger.split('-')[0].toUpperCase();
  const reactionServiceName = area.reactions[0].split('-')[0].toUpperCase();

  const triggerService = services.find(s => s.name.toUpperCase() === triggerServiceName);
  const reactionService = services.find(s => s.name.toUpperCase() === reactionServiceName);

  const triggerAuth = triggerService ? triggerService.connected : false;
  const reactionAuth = reactionService ? reactionService.connected : false;

  const handleActivity = (event) => {
    if (triggerAuth && reactionAuth) {
      API.put(`/area/${area.objectId}/`, {
        "is_actif": event.target.checked,
      }, {
        headers: {
          'Authorization': `Bearer ${getUser().sessionToken}`,
          'Content-Type': 'application/json',
        }
      }).then(response => {
        setActivity(!activity);
      }).catch(error => {
        console.log(error.response);
      })
    } else {
      history.push(getPath('services'));
    }
  };

  const handleDelete = (event) => {
    API.delete(`/area/${area.objectId}/`, {
      headers: {
        'Authorization': `Bearer ${getUser().sessionToken}`,
      }
    }).then(response => {
      window.location.reload();
    }).catch(error => {
      console.log(error);
    })
  }

  const switchClasses = switchStyle();

  return (
    <Paper elevation={3}>
      <Grid container spacing={3}>
        <Grid item>
          <Grid container spacing={2}>
            <Grid item xs={6}>
              <Typography>{triggerServiceName}</Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography>{reactionServiceName}</Typography>
            </Grid>
          </Grid>
        </Grid>
        <Grid item xs={2}>
          <FormControlLabel
            control={
              <Switch
                focusVisibleClassName={switchClasses.focusVisible}
                checked={activity}
                onChange={handleActivity}
                aria-label='activity-switch'
                disableRipple
                classes={{
                  root: switchClasses.root,
                  switchBase: switchClasses.switchBase,
                  thumb: switchClasses.thumb,
                  track: switchClasses.track,
                  checked: switchClasses.checked,
                }}
              />
            }
          />
        </Grid>
        <Grid item>
          <IconButton
            onClick={handleDelete}
            color='secondary'
          >
            <DeleteIcon />
          </IconButton>
        </Grid>
      </Grid>
    </Paper>
  );
}

export default AreaItem;