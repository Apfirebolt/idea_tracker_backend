import axios from 'axios';
import router from '../routes/index';
import { useAuth } from '../store/auth';

let baseURL = 'http://localhost:8000/api/';

const httpClient = axios.create({ baseURL });

export default httpClient;