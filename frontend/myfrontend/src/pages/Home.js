import SearchBar from "./components/SearchBar";
import NavBar from "./components/NavBar";
import Footer from "./components/Footer";
import "./components/styles/homeStyles.css";
import MovieCard from "./components/MovieCard";
import { useEffect, useState } from "react";

const Home = () => {
    const apiKey = "api_key=5ee21d87d3f5a6baef7a499e611db6a4"; // my api-key
    const [list, setList] = useState([]);
    const [homeGenreList, setHomeGenreList] = useState([{}]);
    const [selectedGenres, setSelectedGenres] = useState([]);
    const [currMovies, setCurrMovies] = useState([{}]);

    useEffect(() => {
        setCurrMovies([]);
        setSelectedGenres([]);
        setHomeGenreList([]);
        setList([]);
        //getting the list of all movies from our flask server for our searchbar
        // TODO: change to our db
        fetch(`http://localhost:5002/movies`).then((Response) =>
            Response.json().then((data) => {
                setList(data)
            })
        );

        // getting the list of all genres
        fetch(`https://api.themoviedb.org/3/genre/movie/list?${apiKey}`).then(
            (Response) =>
                Response.json().then((data) => setHomeGenreList(data.genres))
        );
    }, []);

    useEffect(() => { 
        setCurrMovies([]);
        if (selectedGenres.length > 0) {
            fetch(
                // TODO: get movie from our db
                `http://localhost:5002/discovers?genre_ids=${encodeURI(
                    selectedGenres.join(",")
                )}`

                //`https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&${apiKey}&release_date.lte=2023-12-10&with_genres=${encodeURI(
                //    selectedGenres.join(",")
                //)}`

            ).then((Response) =>
                Response.json().then((data) => setCurrMovies(data))
            );


        }
    }, [selectedGenres]);

    const onTagClick = (genreId) => {
        let isPresent = false;
        for (let id of selectedGenres) {
            if (id === genreId) {
                isPresent = true;
                break;
            }
        }
        if (isPresent) {
            setSelectedGenres(
                selectedGenres.filter((item) => item !== genreId)
            );
        } else {
            setSelectedGenres((selectedGenres) => [...selectedGenres, genreId]);
        }
    };
    const renderMovies = () =>
        currMovies.map((movie) => {
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

    return (
        <div className="container-fluid">
            <div className="HomePage">
                <NavBar isHome={false} />
                <div className="HomeSearch">
                    {/*Rendering the searchbar */}
                    <SearchBar movies={list} placeholder="Search for a Movie" />
                </div>

                <h2 className="genreHeader">Magic choices of movies Based On Genre </h2>
                <div className="buttonGrid">
                    {homeGenreList.map((genre) => (
                        <div
                            key={genre.id}
                            onClick={() => onTagClick(genre.id)}
                            className={
                                selectedGenres.includes(genre.id)
                                    ? "genreTagON"
                                    : "genreTagOFF"
                            }
                        >
                            {genre.name}
                            {selectedGenres.includes(genre.id) ? (
                                <i
                                    className="fa fa-times"
                                    aria-hidden="true"
                                ></i>
                            ) : null}
                        </div>
                    ))}
                </div>
            </div>
            {/*Rendering selected genre movies */}
            <div className="container-fluid HomeMovies">
                <div className="container HomeMovieGrid">
                    {currMovies.length > 0 ? renderMovies() : null}
                </div>
            </div>
            <div className="HomeFooter">
                <Footer />
            </div>
        </div>
    );
};

export default Home;