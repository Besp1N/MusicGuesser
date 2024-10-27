import { useContext } from "react";
import { GenreContext } from "../context/GenreContext";

const Result = () => {
    const { genre } = useContext(GenreContext);

    return (
        <div className={"file_genre_display"}>
            Genre: {genre ? genre : "No genre detected yet"}
        </div>
    );
};

export default Result;
