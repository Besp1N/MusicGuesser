import Form from "./components/form.jsx";
import Welcome from "./components/welcome.jsx";
import Result from "./components/result.jsx";

const App = () => {
    return (
        <div className={"main"}>
            <Welcome></Welcome>
            <Result></Result>
            <Form></Form>
        </div>
    )
}

export default App