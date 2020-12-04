import { useState } from 'react'
import useSWR from 'swr'
import { createStyles, makeStyles, useTheme } from '@material-ui/core/styles';
import Autocomplete from '@material-ui/lab/Autocomplete';
import { Card, CircularProgress, TextField, FormControl, Button } from '@material-ui/core'
import './App.css';

const useStyles = makeStyles((theme) =>
  createStyles({
    formControl: {
      margin: theme.spacing(1),
      minWidth: 120,
    },
    chips: {
      display: 'flex',
      flexWrap: 'wrap',
    },
    chip: {
      margin: 2,
    },
  }),
)

function getStyles(index, theme) {
  return {
    fontWeight:
      index === -1
        ? theme.typography.fontWeightRegular
        : theme.typography.fontWeightMedium,
  }
}

const fetcher = (url) => {
  return new Promise(async (resolve, reject) => {
    const res = await fetch(url)

    if (res.ok) {
      const data = await res.json()
      resolve(data)
    } else {
      reject(res.statusText)
    }
  })
}

const App = () => {
  const classes = useStyles();
  const theme = useTheme();

  const [countries, setCountries] = useState([]);

  const { data, error } = useSWR('/api/data', fetcher)

  const handleSubmit = (e) => {
    e.preventDefault()
  }

  const updateCountries = (e) => {
    console.log(e)
  }

  const ITEM_HEIGHT = 48
  const ITEM_PADDING_TOP = 8
  const MenuProps = {
    PaperProps: {
      style: {
        maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
        width: 250,
      },
    },
  }

  if (error) {
    return null
  }

  if (data) {
    console.log(data.grapes)
    return (
      <div className="App">
        <header className="App-header">
          <Card title="Wine recommender" style={{ padding: 40 }}>
            <form action="/" method="POST" onSubmit={handleSubmit}>
              <FormControl className={classes.formControl} onChan>
                <Autocomplete
                  multiple
                  id="tags-standard"
                  options={data.grapes}
                  onChange={updateCountries}
                  renderInput={(params) => (
                    <TextField
                      {...params}
                      variant="standard"
                      label="Multiple values"
                      placeholder="Favorites"
                    />
                  )}
                />
              </FormControl>
              <Button type="submit">
                Submit
              </Button>
            </form>
          </Card>
        </header>
      </div>
    )
  }

  return (
    <div className="App">
      <header className="App-header">
        <CircularProgress />
      </header>
    </div>
  )
}

export default App;
