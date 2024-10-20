import { useState } from "react";

const Form = () => {
    const [file, setFile] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [fileName, setFileName] = useState("Send file to know the genre of your music!");

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        setFile(selectedFile);
        setFileName(selectedFile ? selectedFile.name : "Brak wybranych plików");
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (file) {
            setIsLoading(true);

            // Symuluj operację przesyłania pliku
            setTimeout(() => {
                console.log(file);
                // Po zakończeniu operacji ustaw isLoading na false
                setIsLoading(false);
                // Możesz również zresetować plik
                setFile(null);
                setFileName("Send file to know the genre of your music!");
            }, 2000); // Zmień czas symulacji na rzeczywisty czas operacji
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
}

export default Form;
