import React, { FormEvent, useContext, useEffect, useState } from 'react'
import { createStyles, makeStyles } from '@material-ui/core/styles';
import { Card, Typography, CardHeader, CardMedia, IconButton, ButtonBase, CardContent, Grow } from '@material-ui/core'
import LocalBarIcon from '@material-ui/icons/LocalBar';
import ArrowBackIosIcon from '@material-ui/icons/ArrowBackIos'
import { Rating } from '@material-ui/lab'
import './App.css'
import { resultWinesContext } from './App'

const useStyles = makeStyles((theme) =>
  createStyles({
    heading: {
      display: 'flex',
    },
    backButton: {
      width: 50
    },
    title: {
      width: '100%',
      transform: 'translateX(-25px)'
    },
    wines: {
      display: 'flex',
      flexWrap: 'wrap',
      justifyContent: 'center',
    },
    card: {
      [theme.breakpoints.down('sm')]: {
        margin: 10,
        width: `calc(100% / 1)`,
        maxWidth: 300,
      },
      [theme.breakpoints.up('md')]: {
        margin: 10,
        width: `calc(100% / 2)`,
        maxWidth: 300,
      },
    },
		media: {
			height: 0,
			backgroundSize: 'contain',
			paddingTop: 150,
		},
  }),
)

interface ResultsComponentProps {

}
const Results = (props: ResultsComponentProps) => {
  const classes = useStyles();
  const { wines, setWines } = useContext(resultWinesContext)
  console.log(wines)
  return (
		<>
      <div className={classes.heading}>
        <IconButton
          className={classes.backButton}
          color="primary"
          aria-label="go back"
          onClick={()=>{setWines([])}}
        >
          <ArrowBackIosIcon/>
        </IconButton>
        <Typography variant="h4" className={classes.title}>
          Rekommenderade viner för dig
        </Typography>
      </div>
			<div className={classes.wines}>
        {wines.map((wine, i) =>
          <Grow
            in
            style={{ transformOrigin: '0 0 0' }}
            {...(true ? { timeout: 300 * i + 500 } : {})}
          >
            <Card title={wine.nameBold} className={classes.card} elevation={10.0} key={wine.nameBold + wine.nameThin}>
              <ButtonBase
                style={{ width: '100%', display: 'block', }}
                disableRipple
                onClick={e => window.open(wine.url, '_blank')}
              >
                <CardHeader
                  title={wine.nameBold}
                  subheader={wine.nameThin}
                />
                <CardMedia
                  className={classes.media}
                  image={wine.imageURL + "_100.png"}
                  title={wine.nameBold}
                />
                <CardContent>
                  <Typography variant="body1" color="textSecondary" component="p">
                    {wine.country}
                  </Typography>
                  <Typography variant="body1" component="p">
                    {wine.price} kr
                  </Typography>
                  <Typography variant="body2" color="textSecondary" component="p">
                    {wine.tasteDescription}
                  </Typography>
                </CardContent>
                <Rating
                  name="match"
                  disabled={true}
                  precision={0.1}
                  value={wine.tfidf_score === 0 ? 1 : wine.tfidf_score * 5}
                  icon={<LocalBarIcon />}
                />
              </ButtonBase>
            </Card>
          </Grow>
				)}
			</div>
    </>
  )
}

export default Results
