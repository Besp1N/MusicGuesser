import { useState, useContext } from "react";
import { GenreContext } from "../context/GenreContext";

const Form = () => {
    const [file, setFile] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const { setGenre } = useContext(GenreContext);

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        setFile(selectedFile);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (file) {
            setIsLoading(true);

            const formData = new FormData();
            formData.append("file", file);

            try {
                const response = await fetch("http://127.0.0.1:5000/upload", {
                    method: "POST",
                    body: formData,
                });

                if (response.ok) {
                    const data = await response.json();
                    const genre = data.predictions;
                    setGenre(genre);
                    console.log("Genre:", genre);
                } else {
                    const errorData = await response.json();
                    console.error("Error:", errorData.error || response.statusText);
                    alert(`Error: ${errorData.error || response.statusText}`);
                }
            } catch (error) {
                console.error("Error:", error);
                alert("An error occurred while uploading the file.");
            } finally {
                setIsLoading(false);
                setFile(null);
            }
        } else {
            alert("Please select a file first!");
        }
    };

    return (
        <div className="main_form">
            <div className={"enter_file_sign"}>Enter your file</div>
            <form className={"form_form"} onSubmit={handleSubmit}>
                <input className={"file_input"} type="file" onChange={handleFileChange} />
                <button className={"send_btn"} type="submit" disabled={isLoading}>
                    {isLoading ? "Ładowanie..." : "Wyślij"}
                </button>
            </form>
        </div>
    );
};

export default Form;
