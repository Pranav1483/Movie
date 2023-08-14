import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './styles.css';
import host from '../components/Host';

function LoginPage() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const isActive = localStorage.getItem('9442331fe398b259a1a1dd4ddc062049fca67f4e6d6c783dd838394cb547cb05');
        if (isActive) {
            fetch(host + 'bf1e2a1a0e5ed9da4b836e8d75d490d13e3ae8d46ae048bc961f7bfb358416b3/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: isActive, password: '', status: "no" })
            })
            .then((response) => {
                if (response.status === 404) {
                    localStorage.removeItem('9442331fe398b259a1a1dd4ddc062049fca67f4e6d6c783dd838394cb547cb05');
                    return null;
                }
                else if (response.status === 200) {
                    return response.json();
                }
            })
            .then((data) => {
                if (!data) {
                    return null;
                }
                else {
                    navigate('/', { state: { user: data } });
                }
            })
            .catch((e) => {
                localStorage.removeItem('9442331fe398b259a1a1dd4ddc062049fca67f4e6d6c783dd838394cb547cb05');
            });
        }
    }, [navigate]);

    const handleLogin = (event) => {
        event.preventDefault();
        fetch(host + 'bf1e2a1a0e5ed9da4b836e8d75d490d13e3ae8d46ae048bc961f7bfb358416b3/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username: username, password: password, status: 'yes'})
        })
        .then((response) => {
            if (response.status === 200) {
                return response.json();
            }
            else if (response.status === 401) {
                setError('Wrong Password !');
            }
            else if (response.status === 404) {
                setError('No User Found !');
            }
        })
        .then((data) => {
            localStorage.setItem('9442331fe398b259a1a1dd4ddc062049fca67f4e6d6c783dd838394cb547cb05', data['username']);
            navigate('/', {state: {user: data}});
        })
        .catch(e => {
            setError('Server Error !');
        });
    }

    return (
        <div className="full-container-login">
            <div className="login-container">
                <div className='textbox-container'>
                    <i className="fa-solid fa-user"></i>
                    <input type='text' className='textbox' value={username} onChange={(e) => setUsername(e.target.value)} placeholder='Username'/>
                </div>
                <div className='textbox-container'>
                    <i className="fa-sharp fa-solid fa-key"></i>
                    <input type='password' className='textbox' value={password} onChange={(e) => setPassword(e.target.value)} placeholder='********'/>
                </div>
                <a className='forgot-password' href='/forgotkey'>Forgot Password</a>
                {error && <p className='login-error'>{error}</p>}
                <button className="button-77" onClick={handleLogin}>Login</button>
                <button className="button-77" onClick={() => {navigate('/signup')}}>Sign Up</button>
            </div>
        </div>
    )
}

export default LoginPage;