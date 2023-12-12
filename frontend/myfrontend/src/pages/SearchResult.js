import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import "./components/styles/searchResultsStyles.css";
import MovieCard from "./components/MovieCard";
import NavBar from "./components/NavBar";
import Footer from "./components/Footer";

const SearchResult = () => {
    const params = useParams();
    const apiKey = "api_key=5ee21d87d3f5a6baef7a499e611db6a4"; // my api key
    const inputValue = params.id; // retrieving the searched movie name
    const [searchedMovie, setSearchedMovie] = useState({});
    const [recommendedMovies, setRecommendedMovies] = useState([{}]);
    const [genreList, setGenreList] = useState([{}]);
    const [currGenre, setCurrGenre] = useState([{}]);


    const gotRecommendedData = (apiData) => {
        setRecommendedMovies([]);
        let counter = 16;
        console.log("huahua####\n");
        console.log(apiData);
        // getting data for each of the recommened movies
        for (let movie of apiData.movies) {
            fetch(
                // TODO: db
                `https://api.themoviedb.org/3/search/movie?${apiKey}&query=${movie.title}`
            ).then((Response) =>
                Response.json().then((data) =>
                    setRecommendedMovies((recommendedMovies) => [
                        ...recommendedMovies,
                        data.results[0],
                    ])
                )
            );
            counter--;
            if (counter === 0) break;
        }

    };

    useEffect(
        () => {
            const gotTMDBData = (apiData) => {
                const realMovieData = apiData.results[0];
                setCurrGenre([]);
                setCurrGenre(realMovieData.genre_ids);

                setSearchedMovie(realMovieData);

            };
            // TODO: db query
            fetch(
                `https://api.themoviedb.org/3/search/movie?${apiKey}&query=${inputValue}`
            ).then((Response) =>
                Response.json().then((data) => gotTMDBData(data)) // data in backend returned back should be dict
            );
            
            //####################################
            
            fetch(`http://localhost:5002/similar?movie_title=${encodeURIComponent(inputValue)}`)
            .then((Response) => Response.json())
            .then((data) => {
                console.log("debug###########\n");
                console.log(data);
                if (data.movies && Array.isArray(data.movies)) {
                    gotRecommendedData(data);
                }
            })
            .catch((error) => console.error('Error fetching similar movies:', error));
        

            // TODO: db api
            /*
            fetch(
                `http://localhost:5002/similar?movie_title=${encodeURIComponent(inputValue)}`
            ).then((Response) =>
                Response.json().then((data) => {gotRecommendedData(data);
                ; console.log('mmmmmmmmmmmmmmm');console.log(data.movies)})
            );
*/

            // 
            fetch(
                `https://api.themoviedb.org/3/genre/movie/list?${apiKey}`
            ).then((Response) =>
                Response.json().then((data) => setGenreList(data.genres))
            );
        },
        [inputValue] //Making api call whenever the searched movie changes
    );

    const RenderMovies = () =>
        recommendedMovies.map((movie) => {
            if (movie) {
                return (
                    <MovieCard
                        key={movie.id + movie.original_title}
                        movie={movie}
                    />
                );
            } else {
                return null;
            }
        });
    const displayGenre = () =>
        currGenre.map((movieId, ind) => {
            if (ind >= 3) return null;
            if (movieId) {
                for (let obj of genreList) {
                    if (obj.id === movieId) {
                        if (ind === 2) {
                            return <span>{obj.name}</span>;
                        } else {
                            return (
                                <span>
                                    {obj.name}
                                    {","}{" "}
                                </span>
                            );
                        }
                    }
                }
            } else {
                return null;
            }
            return null;
        });

    const backdropPath = "https://image.tmdb.org/t/p/w1280";

    return (
        <div
            style={{
                backgroundImage: `linear-gradient(to bottom, rgba(0, 0, 0, 0), rgba(0, 0, 0, 1)), url(${backdropPath}${searchedMovie.backdrop_path})`,
            }}
            className="MainBackGround"
        >
            <NavBar isHome={true} />

            <div className="container trailerContainer">
                <div className="container .movie-details">
                    <div className="row ">
                        <div className="col-md-6 left-box col-md-push-6">
                            <h1 className="topTitle-Movie">
                                {searchedMovie.title}{" "}
                            </h1>

                            <p className="overviewContent">
                                {searchedMovie.overview}
                            </p>

                            <div>
                                <b>Rating{" : "}</b>
                                {searchedMovie.vote_average}
                                {"/10 "}

                                <i className="fa-solid fa-star"></i>
                            </div>
                            <div>
                                <b> Release Date </b>
                                {" : "} {searchedMovie.release_date}
                            </div>
                            <div>
                                <b>Genres</b>
                                {" : "}
                                {currGenre ? displayGenre() : null}
                            </div>
                        </div>
                        <div className="col-md-6 col-md-pull-6 text-center">
                            <img
                                className="main-img"
                                src={`https://image.tmdb.org/t/p/w500${searchedMovie.poster_path}`}
                                alt="Movie"
                            />
                        </div>
                    </div>
                </div>
            </div>

            <div className="container-fluid recommendedMovies">
                <h2 className=" container RecommendHeading">
                    Recommended Movies
                </h2>
                {/*Rendering the recommended movie cards */}
                <div className="container recommendedGrid">
                    {RenderMovies()}
                </div>
            </div>
            <Footer />
        </div>
    );
};

export default SearchResult;