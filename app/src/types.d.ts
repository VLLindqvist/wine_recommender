interface WineFormData {
  countries: string[]
  types: string[]
  categoryTastes: string[]
  grapes: string[]
  priceLow: number
  priceHigh: number
}

interface Wine {
  alcoholPercentage: number
  country: string
  district: string
  imageURL: string
  nameBold: string
  nameThin: string
  price: number
  producer: string
  region: string
  type: string
  url: string
  tasteDescription: string
  tfidf_score: number
}

interface WineContext {
  wines: Wine[],
  setWines: React.Dispatch<React.SetStateAction<Wine[]>>
}