import axios from "axios";

const api = axios.create({
    baseURL: "https://qikkbglao9.execute-api.ap-northeast-2.amazonaws.com/test_stage",
    headers: {
        // "x-api-key":"BwmcRlCXDHv1toct0AVGu",
        // 'Access-Control-Allow-Origin': '*'
    }
});


export const lambdaApi = {
    getData: userId => api.get(`/recommend?userid=${userId}`)
};