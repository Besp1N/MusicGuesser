import { useState } from "react";

const Form = () => {
    const [file, setFile] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        setFile(selectedFile);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (file) {
            setIsLoading(true);

            setTimeout(() => {
                console.log(file);
                setIsLoading(false);
                setFile(null);
            }, 2000);
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
