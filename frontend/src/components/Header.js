import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function PageHeader(prop) {
    const [query, setQuery] = useState('');
    const navigate = useNavigate();
    const handleSearch = (event) => {
        event.preventDefault();
        if (query !== '') {
            navigate('/search?query=' + query, {state: {user: prop['user']}})
        }
    }
    const handleLogout = (event) => {
        event.preventDefault();
        localStorage.removeItem('9442331fe398b259a1a1dd4ddc062049fca67f4e6d6c783dd838394cb547cb05');
        navigate('/login');
    }
    const handleLikePage = (event) => {
        event.preventDefault();
        navigate('/likes', {state: {user: prop['user']}})
    }
    const handleBookmarkPage = (event) => {
        event.preventDefault();
        navigate('/watchlist', {state: {user: prop['user']}})
    }
    const handleWatchedPage = (event) => {
        event.preventDefault();
        navigate('/watched', {state: {user: prop['user']}})
    }
    const handleHomePage = (event) => {
        event.preventDefault();
        navigate('/', {state: {user: prop['user']}})
    }

    return (
        <div className="top-header-container">
            <form className="header-form" onSubmit={ handleSearch }>
                <div className="search-container">
                    <button className="search-btn" onClick={ handleSearch }>
                        <i className="fa-solid fa-film"></i>
                    </button>
                    <input type="text" className="search-box" value={query} onChange={(e) => setQuery(e.target.value)}/>  
                </div>
            </form>
            <div className="user-icon-container">
                <button className="user-icon-btn" onClick={handleHomePage}>
                    <i className="fa-solid fa-home"></i>
                </button>
                <button className="user-icon-btn" onClick={handleLikePage}>
                    <i className="fa-sharp fa-solid fa-heart"></i>
                </button>
                <button className="user-icon-btn" onClick={handleBookmarkPage}>
                    <i className="fa-solid fa-bookmark"></i>
                </button>
                <button className="user-icon-btn" onClick={handleWatchedPage}>
                    <i className="fa-solid fa-eye"></i>
                </button>
                <button className="user-icon-btn" onClick={handleLogout}>
                    <i className="fa-solid fa-right-from-bracket"></i>
                </button>
            </div>
        </div>
    )
}

export default PageHeader;