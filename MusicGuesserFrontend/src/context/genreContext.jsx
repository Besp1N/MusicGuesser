import { createContext, useState } from "react";

export const GenreContext = createContext();

// eslint-disable-next-line react/prop-types
export const GenreProvider = ({ children }) => {
    const [genre, setGenre] = useState("");

    return (
        <GenreContext.Provider value={{ genre, setGenre }}>
            {children}
        </GenreContext.Provider>
    );
};
