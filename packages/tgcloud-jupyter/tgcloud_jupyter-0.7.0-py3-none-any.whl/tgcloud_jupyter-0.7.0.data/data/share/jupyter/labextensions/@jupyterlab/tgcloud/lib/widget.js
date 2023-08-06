import { ReactWidget } from '@jupyterlab/apputils';
import ReactDOM from 'react-dom';
import React, { useReducer, useEffect } from 'react';
const LogOut = () => {
    let key = 'token';
    localStorage.removeItem(key);
    const rootElement = document.getElementById('root');
    console.log(rootElement);
    return React.createElement(CounterComponent, null);
};
// load the function
async function loaderFunction() {
    const domain = document.getElementById('domaintigergraph');
    console.log(domain.getAttribute('value'));
    const username = document.getElementById('usernametigergraph').value;
    console.log(username);
    const password = document.getElementById('passwordtigergraph').value;
    console.log(password);
    const graph = document.getElementById('graphs').value;
    console.log(graph);
    let formdata = new FormData();
    formdata.append('username', username);
    formdata.append('password', password);
    formdata.append('host', domain.getAttribute('value'));
    formdata.append('graph', graph);
    const response = await window
        .fetch('http://tigertool.tigergraph.com:5000/loadtobox', {
        method: 'POST',
        body: formdata,
        redirect: 'follow'
    })
        .then(response => response.json())
        .then(result => {
        console.log('Success:', result);
        return result;
    })
        .catch(error => {
        console.error('Error:', error);
        console.log('Error');
    });
    const OutputLive = document.getElementById('outputs');
    if (response['value'] != null) {
        OutputLive.innerHTML =
            OutputLive.innerHTML + '<br>' + 'Algo Loaded Succesfully !';
    }
}
// login to tgcloud box
async function loginFunction() {
    const domain = document.getElementById('domaintigergraph');
    console.log(domain.getAttribute('value'));
    const username = document.getElementById('usernametigergraph').value;
    console.log(username);
    const password = document.getElementById('passwordtigergraph').value;
    console.log(password);
    let formdata = new FormData();
    formdata.append('username', username);
    formdata.append('password', password);
    formdata.append('host', domain.getAttribute('value'));
    const response = await window
        .fetch('http://tigertool.tigergraph.com:5000/loginbox', {
        method: 'POST',
        body: formdata,
        redirect: 'follow'
    })
        .then(response => response.json())
        .then(result => {
        console.log('Success:', result);
        return result;
    })
        .catch(error => {
        console.error('Error:', error);
        console.log('Error');
    });
    const OutputLive = document.getElementById('outputs');
    if (response['value'] != null) {
        // enable algo combo and graphs until login
        const graphsControler = document.getElementById('graphs');
        graphsControler.removeAttribute('disabled');
        graphsControler.innerHTML =
            '<option value=' +
                response['value'] +
                '>' +
                response['value'] +
                '</option>';
        const algControler = document.getElementById('algos');
        algControler.innerHTML = '<option value="AMLSIM">AML Sim</option>';
        algControler.removeAttribute('disabled');
        domain.setAttribute('disabled', 'true');
        document
            .getElementById('usernametigergraph')
            .setAttribute('disabled', 'true');
        document
            .getElementById('passwordtigergraph')
            .setAttribute('disabled', 'true');
        OutputLive.innerHTML =
            OutputLive.innerHTML + '<br>' + 'Connected Succesfully to tgcloud box !';
        OutputLive.innerHTML = OutputLive.innerHTML + '<br>' + 'Graphs Found :';
        OutputLive.innerHTML = OutputLive.innerHTML + '<br>' + response['value'];
    }
}
// open Listing Tabs
function backtoListing() {
    const tabAlgos = document.getElementById('tab2');
    tabAlgos.classList.remove('active');
    tabAlgos.classList.add('inactive');
    const tabMachines = document.getElementById('tab1');
    tabMachines.classList.add('active');
    tabMachines.classList.remove('inactive');
}
// open Algo Tabs
function loaderAlgo(domain, id) {
    const tabAlgos = document.getElementById('tab2');
    tabAlgos.classList.remove('inactive');
    tabAlgos.classList.add('active');
    const tabMachines = document.getElementById('tab1');
    tabMachines.classList.add('inactive');
    tabMachines.classList.remove('active');
    console.log(domain);
    console.log(id);
    const textDomain = document.getElementById('domaintigergraph');
    console.log(textDomain);
    textDomain.setAttribute('value', 'https://' + domain);
    // disabe algo combo and graphs until login
    const graphsControler = document.getElementById('graphs');
    graphsControler.setAttribute('disabled', 'true');
    const algControler = document.getElementById('algos');
    algControler.setAttribute('disabled', 'true');
}
const reducer = (state, action) => {
    switch (action.type) {
        case 'setUsername':
            return Object.assign({}, state, { username: action.payload });
        case 'setPassword':
            return Object.assign({}, state, { password: action.payload });
        case 'setIsButtonDisabled':
            return Object.assign({}, state, { isButtonDisabled: action.payload });
        case 'loginSuccess':
            return Object.assign({}, state, { helperText: action.payload, isError: false });
        case 'loginFailed':
            return Object.assign({}, state, { helperText: action.payload, isError: true });
        case 'setIsError':
            return Object.assign({}, state, { isError: action.payload });
    }
};
const initialState = {
    username: '',
    password: '',
    isButtonDisabled: true,
    helperText: '',
    isError: false
};
const CloudListingComponent = () => {
    useEffect(() => {
        async function anyNameFunction() {
            console.log('Component Loaded ...');
            let key = 'token';
            let token = localStorage.getItem(key);
            console.log(token);
            const listMachines = await getlistmachines(token);
            console.log(listMachines);
            let rows = listMachines['Result'].map(function (d) {
                if (d.State == 'terminated') {
                    return (React.createElement("tr", null,
                        React.createElement("td", null,
                            ' ',
                            React.createElement("img", { src: d.Logo, style: { width: '20px', height: '20px' } }),
                            ' ',
                            React.createElement("input", { type: "hidden", id: "machineID", value: d.ID }),
                            ' ',
                            React.createElement("input", { type: "hidden", id: "machineDomain", value: d.Domain })),
                        React.createElement("td", null, d.Name),
                        React.createElement("td", null, d.Tag),
                        React.createElement("td", null,
                            React.createElement("i", { className: 'fa fa-circle ' + d.State, "aria-hidden": "true" }, ' '),
                            ' ',
                            d.State,
                            ' '),
                        React.createElement("td", null, d.ExternalInstanceType),
                        React.createElement("td", null, d.CreatedAt),
                        React.createElement("td", null, d.UpdatedAt),
                        React.createElement("td", { className: "actions" },
                            React.createElement("i", { className: "fa fa-play", style: { color: 'grey', padding: '10px' }, "aria-hidden": "true" }),
                            React.createElement("i", { className: "fa fa-stop", style: { color: 'grey', padding: '10px' }, "aria-hidden": "true" }),
                            React.createElement("i", { className: "fa fa-tasks", style: { color: 'grey', padding: '10px' }, "aria-hidden": "true" }))));
                }
                if (d.State == 'stopped') {
                    return (React.createElement("tr", null,
                        React.createElement("td", null,
                            ' ',
                            React.createElement("img", { src: d.Logo, style: { width: '20px', height: '20px' } }),
                            ' ',
                            React.createElement("input", { type: "hidden", id: "machineID", value: d.ID }),
                            ' ',
                            React.createElement("input", { type: "hidden", id: "machineDomain", value: d.Domain })),
                        React.createElement("td", null, d.Name),
                        React.createElement("td", null, d.Tag),
                        React.createElement("td", null,
                            React.createElement("i", { className: 'fa fa-circle ' + d.State, "aria-hidden": "true" }, ' '),
                            ' ',
                            d.State,
                            ' '),
                        React.createElement("td", null, d.ExternalInstanceType),
                        React.createElement("td", null, d.CreatedAt),
                        React.createElement("td", null, d.UpdatedAt),
                        React.createElement("td", { className: "actions" },
                            React.createElement("a", { href: "#", onClick: () => opsMachines('start', d.ID) },
                                React.createElement("i", { className: "fa fa-play", style: { padding: '10px' }, "aria-hidden": "true" })),
                            React.createElement("i", { className: "fa fa-stop", style: { color: 'grey', padding: '10px' }, "aria-hidden": "true" }),
                            React.createElement("i", { className: "fa fa-tasks", style: { color: 'grey', padding: '10px' }, "aria-hidden": "true" }))));
                }
                if (d.State == 'ready') {
                    return (React.createElement("tr", null,
                        React.createElement("td", null,
                            ' ',
                            React.createElement("img", { src: d.Logo, style: { width: '20px', height: '20px' } }),
                            ' ',
                            React.createElement("input", { type: "hidden", id: "machineID", value: d.ID }),
                            ' ',
                            React.createElement("input", { type: "hidden", id: "machineDomain", value: d.Domain })),
                        React.createElement("td", null, d.Name),
                        React.createElement("td", null, d.Tag),
                        React.createElement("td", null,
                            React.createElement("i", { className: 'fa fa-circle ' + d.State, "aria-hidden": "true" }, ' '),
                            ' ',
                            d.State,
                            ' '),
                        React.createElement("td", null, d.ExternalInstanceType),
                        React.createElement("td", null, d.CreatedAt),
                        React.createElement("td", null, d.UpdatedAt),
                        React.createElement("td", { className: "actions" },
                            React.createElement("i", { className: "fa fa-play", style: { color: 'grey', padding: '10px' }, "aria-hidden": "true" }),
                            React.createElement("a", { href: "#", onClick: () => opsMachines('stop', d.ID) },
                                React.createElement("i", { className: "fa fa-stop", style: { padding: '10px' }, "aria-hidden": "true" })),
                            React.createElement("a", { href: "#", onClick: () => loaderAlgo(d.Domain, d.ID) },
                                React.createElement("i", { className: "fa fa-tasks", style: { padding: '10px' }, "aria-hidden": "true" })))));
                }
                if (d.State == 'starting' || d.State == 'stopping') {
                    return (React.createElement("tr", null,
                        React.createElement("td", null,
                            ' ',
                            React.createElement("img", { src: d.Logo, style: { width: '20px', height: '20px' } }),
                            ' ',
                            React.createElement("input", { type: "hidden", id: "machineID", value: d.ID }),
                            ' ',
                            React.createElement("input", { type: "hidden", id: "machineDomain", value: d.Domain })),
                        React.createElement("td", null, d.Name),
                        React.createElement("td", null, d.Tag),
                        React.createElement("td", null,
                            React.createElement("i", { className: 'fa fa-circle ' + d.State, "aria-hidden": "true" }, ' '),
                            ' ',
                            d.State,
                            ' '),
                        React.createElement("td", null, d.ExternalInstanceType),
                        React.createElement("td", null, d.CreatedAt),
                        React.createElement("td", null, d.UpdatedAt),
                        React.createElement("td", { className: "actions" },
                            React.createElement("i", { className: "fa fa-play", style: { color: 'grey', padding: '10px' }, "aria-hidden": "true" }),
                            React.createElement("i", { className: "fa fa-stop", style: { color: 'grey', padding: '10px' }, "aria-hidden": "true" }),
                            React.createElement("i", { className: "fa fa-tasks", style: { color: 'grey', padding: '10px' }, "aria-hidden": "true" }))));
                }
            });
            console.log(rows);
            const rowsElement = document.getElementById('rows');
            ReactDOM.render(rows, rowsElement);
        }
        try {
            setInterval(async () => {
                console.log('refreshing !!');
                anyNameFunction();
                console.log('refreshed !!');
            }, 5000);
        }
        catch (e) {
            console.log(e);
        }
    }, []);
    return (React.createElement("div", { id: "listing", className: "listingStyle" },
        React.createElement("title", null, "AWS"),
        React.createElement("meta", { charSet: "utf-8" }),
        React.createElement("meta", { name: "viewport", content: "width=device-width, initial-scale=1" }),
        React.createElement("link", { rel: "stylesheet", href: "https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" }),
        React.createElement("link", { rel: "stylesheet", href: "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" }),
        React.createElement("style", { type: "text/css", dangerouslySetInnerHTML: {
                __html: "\n\t\t  /* MOBILE style */\n\t@media screen and (max-width: 992px) {\n\t    /*\n\t     * In Mobile, hide the tabs controls and undo some potential damage done by the accordion\n\t     */\n\t    .responsive-tabs .nav-tabs,\n\t    .responsive-tabs .tab-content .collapse.active:not(.in) {\n\t        display: none;\n\t    }\n\t    .responsive-tabs .tab-content .collapse.in,\n\t    .responsive-tabs .tab-content .collapsing {\n\t        display: block;\n\t    }\n\t}\n\n\n\t/* DESKTOP style */\n\t@media screen and (min-width: 991px) {\n\t    /*\n\t     * In desktop, hide the accordion's controls and undo some potential damage done on the active tab\n\t     */\n\t    .responsive-tabs .panel-heading {\n\t        display: none;\n\t    }\n\t    .responsive-tabs > .active {\n\t        height: auto !important;\n\t    }\n\t}\n\n\n\t/* To make it a bit prettier */\n\tbody {\n\t    padding: 15px;\n\t}\n\thtml , body {\n\t\theight: 100%;\n    \tbackground: #f7f7f7;\n\t}\n\t.tab-content .panel-heading {\n\t    padding: 0;\n\t}\n\n\t.tab-content a {\n\t    display: block;\n\t    margin-bottom: -1px;\n\t    padding: 10px 15px;\n\t    border: solid #ccc;\n\t    border-width: 1px 0;\n\t}\n\t.table{\n\t\tbackground: #ffffff;\n\t\tbox-shadow: 2px 2px 5px #aaaaaa;\n\t}\n\t.welcome{\n\t\tpadding: 3px;\n\t    background: #ffffff;\n\t    box-shadow: 2px 2px 5px #aaaaaa;\n\t    border-radius: 5px;\n\t    border-left: 10px solid #e15f5f;\n\t}\n\t.nav-tabs{\n\t\tmargin:1%;\n\t}\n\t.welcome p{\n\t    padding: 1%;\n\t    color: #f17790;\n\t    margin: 0;\n\t}\n\t#tab1 h4{\n\t\tmargin: 2% 0;\n\t}\n\t#tab1 i.fa-compass{\n\t\tcolor: #faa70e;\n\t}\n\t.fa-file-alt{\n\t\tcolor: #3a8be5;\n\t}\n\t.actions-ul{\n\t\tlist-style: none;\n\t    padding: 5px 25px;\n\t    padding: 0px;\n\t    box-shadow: 2px 2px 5px #aaaaaa;\n\t    width: max-content;\n\t}\n\t.actions-ul li a{\n\t    padding: 5px 25px;\n\t}\n\t"
            } }),
        React.createElement("div", { className: "responsive-tabs" },
            React.createElement("div", { className: "logout" },
                React.createElement("a", { href: "#", onClick: LogOut, className: "btn btn-info btn-lg" },
                    React.createElement("span", { className: "glyphicon glyphicon-log-out" }),
                    " Log out")),
            React.createElement("ul", { className: "nav nav-tabs", role: "tablist" },
                React.createElement("li", { role: "presentation", className: "active" },
                    React.createElement("a", { href: "#", "aria-controls": "tab1", onClick: () => backtoListing(), role: "tab", "data-toggle": "tab" }, "Machines")),
                React.createElement("li", { role: "presentation" },
                    React.createElement("a", { href: "#", "aria-controls": "tab2", role: "tab", "data-toggle": "tab" }, "Algo Loader"))),
            React.createElement("div", { className: "welcome" },
                React.createElement("p", null, "Welcome to TigerGraph Cloud!")),
            React.createElement("div", { id: "tabs-content", className: "tab-content panel-group" },
                React.createElement("div", { className: "panel-heading", role: "tab", id: "heading1" },
                    React.createElement("a", { href: "#tab1", role: "button", "data-toggle": "collapse", "data-parent": "tabs-content", "aria-expanded": "true", "aria-controls": "tab1" }, "Tab 1")),
                React.createElement("div", { id: "tab1", role: "tabpanel", className: "tab-pane active panel-collapse collapse in active", "aria-labelledby": "heading1" },
                    React.createElement("h4", null,
                        "My solutions ",
                        React.createElement("i", { className: "fa fa-compass", "aria-hidden": "true" })),
                    React.createElement("table", { className: "table" },
                        React.createElement("thead", null,
                            React.createElement("tr", null,
                                React.createElement("th", { scope: "col" }),
                                React.createElement("th", { scope: "col" }, "Name"),
                                React.createElement("th", { scope: "col" }, "Tag"),
                                React.createElement("th", { scope: "col" }, "Status"),
                                React.createElement("th", { scope: "col" }, "Instance"),
                                React.createElement("th", { scope: "col" }, "Creation Date"),
                                React.createElement("th", { scope: "col" }, "Last Upadated"),
                                React.createElement("th", { scope: "col" },
                                    "Actions ",
                                    React.createElement("i", { className: "fa fa-cog", "aria-hidden": "true" })))),
                        React.createElement("tbody", { id: "rows" }))),
                React.createElement("div", { className: "panel-heading", role: "tab", id: "heading2" },
                    React.createElement("a", { href: "#tab2", className: "collapsed", role: "button", "data-toggle": "collapse", "data-parent": "tabs-content", "aria-expanded": "true", "aria-controls": "tab2" }, "Tab 2")),
                React.createElement("div", { id: "tab2", role: "tabpanel", className: "tab-pane panel-collapse collapse inactive", "aria-labelledby": "heading2" },
                    React.createElement("div", { className: "training" },
                        React.createElement("div", { className: "load-block form-group" },
                            React.createElement("input", { type: "text", name: "host", id: "domaintigergraph", value: "", className: "form-control", disabled: true }),
                            React.createElement("input", { type: "text", name: "mail", id: "usernametigergraph", placeholder: "tigergraph", className: "form-control" }),
                            React.createElement("input", { type: "password", name: "password", id: "passwordtigergraph", className: "form-control", placeholder: "Password" }),
                            React.createElement("a", { href: "#", className: "btn btn-info btn-lg", onClick: loginFunction }, "Connect")),
                        React.createElement("div", { className: "form-group", id: "AlgoControler" },
                            React.createElement("h5", null, "Graph"),
                            React.createElement("select", { id: "graphs", className: "form-control" },
                                React.createElement("option", null, "-"),
                                React.createElement("option", null, "-")),
                            React.createElement("h5", null, "Algorithm"),
                            React.createElement("select", { id: "algos", className: "form-control" },
                                React.createElement("option", null, "-"),
                                React.createElement("option", null, "-")),
                            React.createElement("a", { href: "#", className: "btn btn-info btn-lg", onClick: loaderFunction }, "Load"))),
                    React.createElement("div", { className: "live-output" },
                        React.createElement("p", null, "Live output"),
                        React.createElement("p", { id: "outputs" })))))));
};
// Login Component
const CounterComponent = () => {
    const [state, dispatch] = useReducer(reducer, initialState);
    useEffect(() => {
        if (state.username.trim() && state.password.trim()) {
            dispatch({
                type: 'setIsButtonDisabled',
                payload: false
            });
        }
        else {
            dispatch({
                type: 'setIsButtonDisabled',
                payload: true
            });
        }
    }, [state.username, state.password]);
    const boxlogin = {
        padding: '10px',
        backgroundColor: '#fefefe',
        fontFamily: 'Arial',
        fontsize: '10px'
    };
    async function handleLogin() {
        let formdata = new FormData();
        formdata.append('username', state.username);
        formdata.append('password', state.password);
        const rootLoader = document.getElementById('Loader');
        rootLoader.classList.add('active');
        const response = await window
            .fetch('http://tigertool.tigergraph.com:5000/login', {
            method: 'POST',
            body: formdata,
            redirect: 'follow'
        })
            .then(response => response.json())
            .then(result => {
            console.log('Success:', result);
            return result;
        })
            .catch(error => {
            console.error('Error:', error);
            dispatch({
                type: 'loginFailed',
                payload: 'Incorrect username or password'
            });
            console.log('Error');
        });
        // handling results
        if (response['Hello'] == 'tgcloud') {
            let key = 'token';
            localStorage.setItem(key, response['token']);
            rootLoader.classList.remove('active');
            const rootElement = document.getElementById('root');
            ReactDOM.render(React.createElement(CloudListingComponent, null), rootElement);
        }
        else {
            dispatch({
                type: 'loginFailed',
                payload: 'Incorrect username or password'
            });
            console.log('Error');
            rootLoader.classList.remove('active');
        }
    }
    const handleKeyPress = (event) => {
        if (event.keyCode === 13 || event.which === 13) {
            state.isButtonDisabled || handleLogin();
        }
    };
    const handleUsernameChange = event => {
        dispatch({
            type: 'setUsername',
            payload: event.target.value
        });
    };
    const handlePasswordChange = event => {
        dispatch({
            type: 'setPassword',
            payload: event.target.value
        });
    };
    const mystyle = {
        color: 'white',
        backgroundColor: 'DodgerBlue',
        fontFamily: 'Arial'
    };
    const mystyleButton = {
        color: 'white',
        padding: '10px 0',
        backgroundColor: 'DodgerBlue',
        width: '100%',
        height: '100%',
        fontFamily: 'Arial'
    };
    const rootContainer = {
        width: '100%',
        height: '100%'
    };
    return (React.createElement("div", { id: "root", style: rootContainer },
        React.createElement("div", { id: "Loader", className: "Loader" },
            React.createElement("div", { className: "spinner" })),
        React.createElement("div", { className: "container" },
            React.createElement("div", { className: "mat-toolbar mat-primary mat-toolbar-single-row" }, "TigerGraph Cloud"),
            React.createElement("div", { className: "container-mini" },
                React.createElement("form", { style: boxlogin, noValidate: true, autoComplete: "off" },
                    React.createElement("img", { width: "50%", src: "https://tgcloud.io/assets/img/tgcloud-logo.png" }),
                    React.createElement("h3", null, "TigerGraph Cloud"),
                    React.createElement("br", null),
                    React.createElement("div", { className: "form-group" },
                        React.createElement("input", { id: "username", type: "email", className: "texts", placeholder: "Enter email", onChange: handleUsernameChange, onKeyPress: handleKeyPress })),
                    React.createElement("div", { className: "form-group" },
                        React.createElement("input", { id: "password", type: "password", className: "texts", placeholder: "Enter password", onChange: handlePasswordChange, onKeyPress: handleKeyPress })),
                    React.createElement("br", null),
                    React.createElement("div", { style: mystyle, className: "btn btn-primary btn-block" },
                        React.createElement("button", { style: mystyleButton, type: "button", onClick: handleLogin, disabled: state.isButtonDisabled }, "Sign in")),
                    React.createElement("p", { className: "forgot-password text-right" },
                        "Forgot ",
                        React.createElement("a", { href: "#" }, "password?")))))));
};
// Getting the Machines from tgcloud
async function getlistmachines(token) {
    let formdata = new FormData();
    formdata.append('token', token);
    const listMachines = await window
        .fetch('http://tigertool.tigergraph.com:5000/list', {
        method: 'POST',
        body: formdata,
        redirect: 'follow'
    })
        .then(response => response.json())
        .then(result => {
        console.log(result);
        if (result['error'] == 401) {
            localStorage.removeItem('token');
            ReactDOM.render(React.createElement(CounterComponent, null));
        }
        else {
            return result;
        }
    })
        .catch(error => {
        console.log('Error');
    });
    return listMachines;
}
async function opsMachines(action, id_machine) {
    let key = 'token';
    const token = localStorage.getItem(key);
    let formdata = new FormData();
    formdata.append('token', token);
    formdata.append('id_machine', id_machine);
    formdata.append('action', action);
    const listMachines = await window
        .fetch('http://tigertool.tigergraph.com:5000/ops', {
        method: 'POST',
        body: formdata,
        redirect: 'follow'
    })
        .then(response => response.json())
        .then(result => {
        console.log(result);
        if (result['error'] == 401) {
            localStorage.removeItem('token');
            ReactDOM.render(React.createElement(CounterComponent, null));
        }
        else {
            return result;
        }
    })
        .catch(error => {
        console.log('Error');
    });
    return listMachines;
}
export class CounterWidget extends ReactWidget {
    constructor() {
        super();
        this.addClass('jp-ReactWidget');
    }
    render() {
        let key = 'token';
        let token = localStorage.getItem(key);
        // check if token is ok ??? ToDo :
        if (token != null) {
            return React.createElement(CloudListingComponent, null);
        }
        else {
            return React.createElement(CounterComponent, null);
        }
    }
}
