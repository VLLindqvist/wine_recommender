import React, { createContext, useState } from 'react'
import useSWR from 'swr'
import { createStyles, makeStyles } from '@material-ui/core/styles';
import NotInterestedIcon from '@material-ui/icons/NotInterested';
import { CircularProgress, Typography, Slide, Dialog } from '@material-ui/core'
import { TransitionProps } from '@material-ui/core/transitions';

import './App.css';
import Form from './Form';
import Results from './Results';
import fetcher from './fetcher';

export const resultWinesContext = createContext<WineContext>({
  wines: [],
  setWines: () => {}
})

const SlideTransition = React.forwardRef(function Transition(
  props: TransitionProps & { children?: React.ReactElement<any, any> },
  ref: React.Ref<unknown>,
) {
  return <Slide direction="right" ref={ref} {...props} />;
})

const useStyles = makeStyles((theme) =>
  createStyles({
    results: {
      // position: 'absolute',
      top: 0,
      bottom: 0,
      left: 0,
      right: 0,
    },
    form: {
      // position: 'absolute',
      top: 0,
      bottom: 0,
      left: 0,
      right: 0,
    },
    backdrop: {
      backgroundColor: 'transparent',
    },
  }),
)

const App = () => {
  const classes = useStyles();
  const [wines, setWines] = useState<Wine[]>([])

  const { data, error } = useSWR<WineFormData>('/api/data', fetcher)

  return (
    <resultWinesContext.Provider value={{ wines, setWines}}>
      <div className="app">
        {!error && !data &&
          <header className="appHeader">
            <CircularProgress />
          </header>
        }
        {data !== undefined && 
          <div className="appContainer">
            {wines && wines.length > 0 &&
              <div className={classes.results}>
                <Results/>
              </div>
            }
            <div className={classes.form}>
              <Dialog
                open={!wines.length}
                TransitionComponent={SlideTransition}
                keepMounted
                onClose={() => {}}
                aria-labelledby="alert-dialog-slide-title"
                aria-describedby="alert-dialog-slide-description"
                BackdropProps={{
                  classes: {
                  root: classes.backdrop
                  }
                }}
              >
                <div>
                  <Form data={data} />
                </div>
              </Dialog>
            </div>
          </div>
        }
        {error &&
          <div className="appHeader">
            <NotInterestedIcon />
            <Typography variant="h4">
              Refresh this page.
            </Typography>
          </div>
        }
      </div>
    </resultWinesContext.Provider>
  )
}

export default App;
