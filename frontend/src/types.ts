// frontend/src/types.ts

// Interface for individual source metadata within a topic's articles
export interface SourceData {
    name?: string; // name property can be optional as per some API responses
}

// Interface for a single article's metadata (useful for topic.articles list)
export interface ArticleMetadata {
    title?: string;
    source?: SourceData;
    url?: string;
}

// Interface for a Topic object within a Sector
export interface TopicData {
    name: string;
    one_sentence_description: string; // Short description for mid-level display
    summary: string; // Multi-paragraph detailed summary
    sources: SourceData[]; // Array of source objects that contributed to this topic
    urls: string[]; // Array of URLs corresponding to the sources
    importance: number; // Importance score from backend (1-10)
}

// Interface for a Sector's data
export interface SectorData {
    landingSummary: string; // High-level 3-sentence summary for the landing page
    topics: TopicData[]; // List of TopicData objects within this sector
}

// Interface for the overall news data structure returned by the backend
export interface NewsData {
    [sectorName: string]: SectorData; // Dynamically keys by sector name
}

// Define the MARKET_SECTORS array here as it's used by both backend and frontend
export const MARKET_SECTORS: string[] = [
    "Technology & Software",
    "Finance & Economy",
    "Healthcare & Biotech",
    "Energy & Materials",
    "Defense & Geopolitics",
    "Cryptocurrency & Blockchain",
    "Artificial Intelligence & Robotics",
    "Retail & Consumer Goods",
    "Automotive & Mobility",
    "Real Estate & Infrastructure"
];