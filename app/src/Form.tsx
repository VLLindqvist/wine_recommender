import React, { FormEvent, useEffect, useState, useContext } from 'react'
import useSWR from 'swr'
import { createStyles, makeStyles } from '@material-ui/core/styles';
import MuiAutocomplete from '@material-ui/lab/Autocomplete';
import { Card, CircularProgress, TextField, FormControl, Button, Typography, Slider, Slide } from '@material-ui/core'
import './App.css';
import { resultWinesContext } from './App';

const useStyles = makeStyles((theme) =>
  createStyles({
    card: {
      padding: 40,
      width: "100vw",
      maxWidth: 600,
    },
    formWrap: {
      width: "100%",
      display: "flex",
      flexDirection: "column",
    },
    formControl: {
      padding: theme.spacing(1),
      width: "100%",
      maxHeight: 300,
    },
    chips: {
      display: 'flex',
      flexWrap: 'wrap',
    },
    chip: {
      margin: 2,
    },
    buttonContainer: {
      width: "100%",
      display: "flex",
      justifyContent: "center",
    }
  }),
)

const numFormatter = (num: number): string => {
  if (num > 9999) {
    return (num / 1000).toFixed(0) + "K"; // convert to K for number from > 1000 < 1 million
  }
  
  return num.toString(); // if value < 1000, nothing to do
}

interface FormComponentProps {
  data: WineFormData
}
const Form = ({ data }: FormComponentProps) => {
  const classes = useStyles();
  const { setWines } = useContext(resultWinesContext)

  const [selectedCountries, setSelectedCountries] = useState<string[]>([])
  const [selectedTypes, setSelectedTypes] = useState<string[]>([])
  const [selectedCategories, setSelectedCategories] = useState<string[]>([])
  const [selectedGrapes, setSelectedGrapes] = useState<string[]>([])
  const [priceRangePercentage, setPriceRangePercentage] = useState<number[]>([0, 100])
  const [priceRange, setPriceRange] = useState<number[]>([0, 50000])
  const [hasUpdatedPrice, setHasUpdatedPrice] = useState<boolean>(false)
  const [tasteDescription, setTasteDescription] = useState<string>("")

  useEffect(() => {
    if (data && !hasUpdatedPrice) {
      setPriceRange([data.priceLow, data.priceHigh])
      setHasUpdatedPrice(true)
    }
  }, [data, hasUpdatedPrice])

  useEffect(() => {
    if (data) {
      const newLow: number = (priceRangePercentage[0] / 100) * data.priceHigh
      const newMax: number = (priceRangePercentage[1] / 100) * data.priceHigh
      setPriceRange([newLow, newMax])
    }
  }, [data, priceRangePercentage])

  useEffect(() => {
    console.log(priceRange)
  }, [priceRange])

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    
    const res = await fetch('/api/recommend', {
      "method": "POST",
      "headers": { 'Content-Type': 'application/json' },
      "body": JSON.stringify({
        countries: selectedCountries,
        types: selectedTypes,
        categoryTastes: selectedCategories,
        grapes: selectedGrapes,
        priceLow: priceRange[0],
        priceHigh: priceRange[1],
        tasteDescription
      })
    })

    if (res.ok) {
      const data: { results: Wine[] } = await res.json()
      setWines(data.results)
    } else {}
  }

  return (
    <Card title="Vinrekommendation" className={classes.card}>
      <Typography variant="h4">
        Vinrekommendation
      </Typography>

      <form action="/" method="POST" onSubmit={handleSubmit} className={classes.formWrap}>
        <FormControl className={classes.formControl}>
          <Autocomplete<string[]>
            setState={setSelectedCountries}
            data={data.countries}
            label="Land"
          />
        </FormControl>
        <FormControl className={classes.formControl}>
          <Autocomplete<string[]>
            setState={setSelectedTypes}
            data={data.types}
            label="Typ"
          />
        </FormControl>
        <FormControl className={classes.formControl}>
          <Autocomplete<string[]>
            setState={setSelectedCategories}
            data={data.categoryTastes}
            label="Kategori"
          />
        </FormControl>
        <FormControl className={classes.formControl}>
          <Autocomplete<string[]>
            setState={setSelectedGrapes}
            data={data.grapes}
            label="Druvor"
          />
        </FormControl>
        <FormControl className={classes.formControl} style={{ alignItems: "flex-start" }}>
          <Typography gutterBottom>
            Pris
          </Typography>
          <Slider
            value={priceRangePercentage}
            onChange={(e, newValue) => {setPriceRangePercentage(newValue as number[])}}
            valueLabelDisplay="auto"
            aria-labelledby="range-slider"
            // max={data.priceHigh}
            scale={(x) => Math.floor((x/100) * data.priceHigh)}
            // scale={(x) => x ** 5}
            valueLabelFormat={numFormatter}
            // getAriaValueText={valuetext}
          />
        </FormControl>
        <FormControl className={classes.formControl}>
          <TextField
            value={tasteDescription}
            onChange={(e) => {setTasteDescription(e.currentTarget.value)}}
            id="outlined-textarea"
            label="Dina smakpreferenser"
            // placeholder="Placeholder"
            multiline
            variant="outlined"
          />
        </FormControl>
        <div className={classes.buttonContainer}>
          <Button type="submit" variant="contained">
            Hitta viner
          </Button>
        </div>
      </form>
    </Card>
  )
}

interface AutocompleteProps<T> {
  setState: React.Dispatch<React.SetStateAction<T>>
  data: T
  label: string
}
function Autocomplete<T>(props: AutocompleteProps<T>) {
  return (
    <MuiAutocomplete
      multiple
      id="tags-standard"
      options={props.data as any}
      onChange={(e, newValue) => {props.setState((newValue as any) as T)}}
      renderInput={(params) => (
        <TextField
          {...params}
          variant="standard"
          label={props.label}
        />
      )}
    />
  )
}

export default Form
