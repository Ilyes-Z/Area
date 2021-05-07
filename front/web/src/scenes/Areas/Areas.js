import React, { useEffect, useState } from 'react';

import API from 'api';
import getUser from 'services/user/getUser';
import { Container, Grid, makeStyles, Typography } from '@material-ui/core';

import AreaItem from 'components/AreaItem/AreaItem';
import { useHistory } from 'react-router-dom';

const useStyles = makeStyles(theme => ({
  title: {
    marginTop: theme.spacing(5),
    fontWeight: "bold",
  },
  item: {
    marginTop: theme.spacing(5),
  }
}))

function Areas() {

  const [areas, setAreas] = useState([]);
  const [services, setServices] = useState([]);

  const history = useHistory();

  useEffect(() => {
    API.get('/area/', {
      headers: {
        'Authorization': `Bearer ${getUser().sessionToken}`,
      }
    }).then(response => {
      setAreas(response.data);
    }).catch(response => {
      console.log(response);
    })

    API.get('/services?auth=true', {
      headers: {
        'Authorization': `Bearer ${getUser().sessionToken}`,
      }
    }).then(response => {
      setServices(response.data.results || []);
    }).catch(response => {
      console.log(response.data);
    })
  }, []);

  const classes = useStyles();

  return (
    <Container component='main' maxWidth='md'>
      <Typography className={classes.title} component="h1" variant="h4">
        Areas
      </Typography>
      <Grid container justify='center' spacing={2}>
        {areas.map((area, key) => {
          return (
            <Grid item xs={12} key={key} className={classes.item}>
              <AreaItem area={area} services={services} services={services} history={history} />
            </Grid>
          );
        })}
      </Grid>
    </Container>
  );
}

export default Areas;