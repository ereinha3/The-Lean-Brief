// frontend/src/App.tsx

import React, { useState, useEffect } from 'react';
import './index.css'; // Ensure Tailwind CSS is imported here
import { NewsData, SectorData, TopicData, MARKET_SECTORS } from './types'; // Import types and sectors

// The main App component for The Lean Brief
function App() {
    const [newsData, setNewsData] = useState<NewsData | null>(null); // Explicitly typed
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    const [selectedSector, setSelectedSector] = useState<string | null>(null); // Sector name string
    const [selectedTopic, setSelectedTopic] = useState<TopicData | null>(null); // TopicData object

    // Effect hook to fetch data from the backend when the component mounts
    useEffect(() => {
        const fetchSummaries = async () => {
            try {
                setLoading(true);
                setError(null);
                
                const response = await fetch('http://localhost:5000/api/summarize_news', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });
                
                if (!response.ok) {
                    const errorText = await response.text();
                    throw new Error(`Backend Error: ${response.status} - ${errorText.substring(0, 100)}...`);
                }
                
                const data: NewsData = await response.json(); // Cast to NewsData type
                setNewsData(data);
            } catch (err: any) { // Use 'any' or check error type if necessary
                console.error("Failed to fetch news summaries:", err);
                setError(err.message || 'Failed to connect to the backend server. Please ensure the backend is running on http://localhost:5000');
            } finally {
                setLoading(false);
            }
        };

        fetchSummaries();
    }, []);

    // Handler to open the detail view for a specific sector
    const handleSectorClick = (sectorName: string) => {
        setSelectedSector(sectorName);
        setSelectedTopic(null); // Ensure topic modal is closed when new sector is selected
    };

    // Handler to open the detail modal for a specific topic
    const handleTopicClick = (topic: TopicData) => {
        setSelectedTopic(topic);
    };

    // Handler to close the topic detail modal
    const closeTopicModal = () => {
        setSelectedTopic(null);
    };

    // Handler to go back from sector detail to main landing page
    const goBackToSectors = () => {
        setSelectedSector(null);
        setSelectedTopic(null);
    };

    // Handler to refresh data
    const refreshData = async () => {
        try {
            setLoading(true);
            setError(null);
            
            const response = await fetch('http://localhost:5000/api/summarize_news', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Backend Error: ${response.status} - ${errorText.substring(0, 100)}...`);
            }
            
            const data: NewsData = await response.json();
            setNewsData(data);
        } catch (err: any) {
            console.error("Failed to refresh news summaries:", err);
            setError(err.message || 'Failed to connect to the backend server. Please ensure the backend is running on http://localhost:5000');
        } finally {
            setLoading(false);
        }
    };

    // Display loading state
    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-indigo-50 to-blue-50 text-indigo-700">
                <div className="flex flex-col items-center">
                    <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-indigo-500"></div>
                    <p className="mt-4 text-xl font-semibold">Gathering the brief...</p>
                    <p className="text-sm text-gray-500 mt-2">This may take a moment as we process the latest news.</p>
                </div>
            </div>
        );
    }

    // Display error state
    if (error) {
        return (
            <div className="flex flex-col items-center justify-center min-h-screen bg-red-50 text-red-800 p-8">
                <h2 className="text-3xl font-bold mb-4">Oops! Something Went Wrong</h2>
                <p className="text-lg text-center mb-6">Failed to load market summaries:</p>
                <p className="font-mono bg-red-100 p-4 rounded-lg text-sm max-w-xl text-center break-words">{error}</p>
                <p className="mt-6 text-base text-gray-700">
                    Please ensure your backend server is running on `http://localhost:5000`
                    and check its console for detailed error messages (e.g., API key issues, rate limits).
                </p>
            </div>
        );
    }

    // Main application rendering
    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 text-gray-900 font-inter antialiased">
            {/* Header Section */}
            <header className="bg-white shadow-md py-5 px-6 sticky top-0 z-10">
                <div className="max-w-7xl mx-auto flex justify-between items-center">
                    <h1 className="text-4xl font-extrabold text-indigo-700 font-display">The Lean Brief</h1>
                    <button
                        onClick={refreshData}
                        disabled={loading}
                        className="px-4 py-2 bg-indigo-500 text-white rounded-lg hover:bg-indigo-600 transition-colors duration-200 font-semibold shadow-lg focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:ring-opacity-75 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
                    >
                        {loading ? (
                            <>
                                <div className="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-white mr-2"></div>
                                Refreshing...
                            </>
                        ) : (
                            <>
                                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                                </svg>
                                Refresh
                            </>
                        )}
                    </button>
                </div>
            </header>

            {/* Main Content Area */}
            <main className="max-w-7xl mx-auto py-10 px-6">
                {!selectedSector ? (
                    // Landing Page: Sector Overview
                    <>
                        <h2 className="text-5xl font-extrabold text-gray-800 mb-12 text-center leading-tight">
                            Your Macro Market Snapshot
                        </h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                            {MARKET_SECTORS.map(sectorName => {
                                // Get sector data, provide a fallback if not found
                                const sectorData: SectorData = newsData?.[sectorName] || { landingSummary: "No recent news observed for this sector.", topics: [] };
                                return (
                                    <div
                                        key={sectorName}
                                        className="bg-white rounded-2xl shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 cursor-pointer p-7 flex flex-col justify-between border border-blue-100"
                                        onClick={() => handleSectorClick(sectorName)}
                                    >
                                        <h3 className="text-2xl font-bold text-indigo-600 mb-3">{sectorName}</h3>
                                        <p className="text-gray-700 text-base leading-relaxed flex-grow mb-5">
                                            {sectorData.landingSummary}
                                        </p>
                                        <button className="self-start px-6 py-2 bg-indigo-500 text-white rounded-full hover:bg-indigo-600 transition-colors duration-200 font-semibold shadow-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:ring-opacity-75">
                                            Dive Deeper
                                        </button>
                                    </div>
                                );
                            })}
                        </div>
                    </>
                ) : (
                    // Sector Detail Page: List of Topics
                    <div className="animate-fade-in-up">
                        <button
                            onClick={goBackToSectors}
                            className="text-indigo-600 hover:text-indigo-800 text-lg font-semibold flex items-center mb-8 px-4 py-2 rounded-full border border-indigo-200 hover:bg-indigo-50 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-indigo-300"
                        >
                            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
                            Back to All Sectors
                        </button>
                        <h2 className="text-5xl font-extrabold text-gray-800 mb-10 text-center leading-tight">
                            {selectedSector} Brief
                        </h2>

                        <div className="space-y-6">
                            {/* Use optional chaining for newsData[selectedSector] */}
                            {newsData && selectedSector && newsData[selectedSector]?.topics.length > 0 ? (
                                // Sort topics by importance (1 is most important, so lowest number)
                                [...(newsData[selectedSector]?.topics || [])].sort((a, b) => a.importance - b.importance).map((topic: TopicData, index: number) => (
                                    <div
                                        key={index}
                                        className="bg-white rounded-xl shadow-md hover:shadow-lg transition-all duration-300 transform hover:scale-[1.005] cursor-pointer p-6 border-l-4 border-indigo-400 flex flex-col justify-between"
                                        onClick={() => handleTopicClick(topic)}
                                    >
                                        <h3 className="text-xl font-semibold text-gray-900 mb-2">{topic.name}</h3>
                                        <p className="text-gray-700 text-base leading-relaxed flex-grow mb-4">
                                            {topic.one_sentence_description}
                                        </p>
                                        <div className="flex justify-between items-center text-sm text-gray-500">
                                            <span className="font-medium text-indigo-500">
                                                Importance: {topic.importance}/10
                                            </span>
                                            <button className="px-4 py-1.5 bg-indigo-100 text-indigo-700 rounded-full text-xs font-medium hover:bg-indigo-200 transition-colors">
                                                Read More
                                            </button>
                                        </div>
                                    </div>
                                ))
                            ) : (
                                <p className="text-center text-gray-600 text-lg py-12 bg-white rounded-xl shadow-md">
                                    No detailed topics available for this sector recently.
                                </p>
                            )}
                        </div>
                    </div>
                )}
            </main>

            {/* Topic Detail Modal */}
            {selectedTopic && (
                <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center p-4 z-50 animate-fade-in">
                    <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-4xl max-h-[90vh] overflow-y-auto relative animate-slide-up">
                        <button
                            onClick={closeTopicModal}
                            className="absolute top-5 right-5 text-gray-500 hover:text-gray-800 text-5xl leading-none font-light transition-colors duration-200 focus:outline-none"
                        >
                            &times;
                        </button>
                        <h2 className="text-4xl font-extrabold text-indigo-700 mb-6 pb-4 border-b-2 border-indigo-100">
                            {selectedTopic.name}
                        </h2>
                        <div className="prose prose-lg max-w-none text-gray-800 leading-relaxed mb-8">
                            {/* Render multi-paragraph summary. Split by double newline for paragraphs. */}
                            {selectedTopic.summary.split('\n\n').map((paragraph: string, idx: number) => (
                                <p key={idx} className="mb-4">{paragraph}</p>
                            ))}
                        </div>
                        <div className="text-sm text-gray-600 border-t pt-4">
                            <p className="font-semibold text-gray-700 mb-2">Original Sources:</p>
                            <ul className="list-disc list-inside space-y-1">
                                {selectedTopic.sources.map((source, index: number) => (
                                    <li key={index}>
                                        <a
                                            href={selectedTopic.urls[index]}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="text-blue-600 hover:underline"
                                        >
                                            {source?.name || 'Unknown Source'}
                                        </a> - {selectedTopic.urls[index]}
                                    </li>
                                ))}
                            </ul>
                            <p className="mt-4 font-medium text-indigo-500">Importance Score: {selectedTopic.importance}/10</p>
                        </div>
                    </div>
                </div>
            )}

            {/* Footer Section */}
            <footer className="bg-gray-800 text-gray-400 py-6 text-center mt-10">
                <div className="max-w-7xl mx-auto px-6">
                    &copy; {new Date().getFullYear()} The Lean Brief. All rights reserved.
                </div>
            </footer>
        </div>
    );
}

export default App;