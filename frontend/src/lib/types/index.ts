export interface KeywordMatch {
  keyword: string;
  found: boolean;
  context: string;
}

export interface WeakPhrase {
  original: string;
  suggestion: string;
  reason: string;
  location: string;
}

export interface Suggestion {
  category: 'impact' | 'keywords' | 'structure' | 'formatting';
  priority: 'high' | 'medium' | 'low';
  title: string;
  description: string;
}

export interface AnalysisResult {
  overall_score: number;
  summary: string;
  keyword_matches: KeywordMatch[];
  weak_phrases: WeakPhrase[];
  suggestions: Suggestion[];
  strengths: string[];
}

export type AnalysisState = 'idle' | 'uploading' | 'analysing' | 'streaming' | 'complete' | 'error';

export interface AppState {
  file: File | null;
  fileName: string;
  jobDescription: string;
  state: AnalysisState;
  result: AnalysisResult | null;
  error: string;
  streamedContent: string;
}
