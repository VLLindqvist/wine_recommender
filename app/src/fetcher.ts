const fetcher = (url: string): Promise<WineFormData> => {
  return new Promise(async (resolve, reject) => {
    const res = await fetch(url)

    if (res.ok) {
      const dataRaw = await res.json()
      console.log(dataRaw)
      let data = Object.assign({}, dataRaw, {
        priceLow: dataRaw.prices[0],
        priceHigh: dataRaw.prices[1],
      })
      delete data.prices

      resolve(data)
    } else {
      reject(res.statusText)
    }
  })
}

export default fetcher