import { Typography, TextField, Grid, makeStyles, Button } from "@material-ui/core"
import Autocomplete from '@material-ui/lab/Autocomplete';
import { useEffect } from "react";
import { useState } from "react";

const useStyles = makeStyles((theme) => ({
  label: {
    paddingTop: "15px",
    paddingBottom: "5px",
    fontWeight: "bold",
  },
}))

function Action({services, handler, index, type, triggerId, ...props}) {

  const [tmp, setTmp] = useState({ service: null, action: null, parameters: {}})

  const handleParameters = (label, event) => {
    	setTmp(prevState => {
        return { ...prevState, parameters: {
          ...prevState.parameters,
          [label]: event.target.value
        }}
      })
  };

  useEffect(() => {
    var save = {
      service: tmp.service ? tmp.service.name : null,
      action: tmp.action && tmp.service ? tmp.action.id : null,
      parameters: tmp.parameters
    };
    handler(save);
  }, [tmp]);

  const classes = useStyles()

  return (
    <Grid container justify="center" spacing={2}>
      <Grid item xs={6}>
        <Typography className={classes.label} component="h4">
          Choose a service...
        </Typography>
        <Autocomplete
          id="service"
          value={tmp.service}
          onChange={(event, newValue) => {
            setTmp({ service: newValue, action: null, parameters: null })
          }}
          options={services}
          getOptionLabel={(option) => option.name}
          renderInput={(params) => <TextField {...params} label="Service" variant="outlined" color="secondary" />}
        />
      </Grid>
      <Grid item xs={6}>
        <Typography className={classes.label} component="h4">
          and his associated action !
        </Typography>
        <Autocomplete
          id="action"
          value={tmp.action}
          onChange={(event, newValue) => {
            setTmp(prevState => {
              var test = {};
              if (newValue) {
                for (var key in newValue.parameters) {
                  test[newValue.parameters[key].name] = null;
                }
              }
              return { ...prevState, action: newValue, parameters: test };
            });
          }}
          disabled={tmp.service ? false : true}
          options={tmp.service ? services.find(service => service.name === tmp.service.name)[type] : []}
          getOptionLabel={(option) => option.name}
          renderInput={(params) => <TextField {...params} label="Action" variant="outlined" color="secondary"/>}
        />
      </Grid>
      {!!tmp.action && tmp.action.parameters.length !== 0 ? (
        <>
          <Grid item xs={12}>
            <Typography className={classes.label} component="h4">
              Give us some details...
            </Typography>
          </Grid>
          {services.find(service => service.name === tmp.service.name)
            [type].find(reaction => reaction.id === tmp.action.id).parameters.map((param, key) => {
              if (type === 'reactions' && param.not_required && param.not_required.includes(triggerId)) return;
              return (
                <Grid key={key} item xs={12}>
                  <TextField
                    value={tmp.parameters[param.name] ? tmp.parameters[param.name] : ""}
                    onChange={(e) => handleParameters(param.name, e)}
                    label={param.name}
                    type={param.type}
                    variant="outlined"
                    color="secondary"
                    fullWidth
                  />
                </Grid>
              )
          })}
        </>
      ) : (<></>)}
    </Grid>
  );
}

export default Action;
