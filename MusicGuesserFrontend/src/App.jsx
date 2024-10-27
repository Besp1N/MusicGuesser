import Form from "./components/form.jsx";
import Welcome from "./components/welcome.jsx";
import Result from "./components/result.jsx";
import {GenreProvider} from "./context/genreContext.jsx";

const App = () => {
    return (
        <GenreProvider>
            <div className={"main"}>
                <Welcome></Welcome>
                <Result></Result>
                <Form></Form>
            </div>
        </GenreProvider>
    )
}

export default App