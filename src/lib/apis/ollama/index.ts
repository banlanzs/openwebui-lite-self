// Ollama API support removed
export const verifyOllamaConnection = async (token: string = '', connection: any = {}) => { return {}; };
export const getOllamaConfig = async (token: string = '') => { return {}; };
export const updateOllamaConfig = async (token: string = '', config: any) => { return {}; };
export const getOllamaUrls = async (token: string = '') => { return []; };
export const updateOllamaUrls = async (token: string = '', urls: string[]) => { return []; };
export const getOllamaVersion = async (token: string, urlIdx?: number) => { return false; };
export const getOllamaModels = async (token: string = '', urlIdx: null | number = null) => { return []; };
export const generatePrompt = async (token: string = '', model: string, conversation: string) => { return null; };
export const generateEmbeddings = async (token: string = '', model: string, text: string) => { return null; };
export const generateTextCompletion = async (token: string = '', model: string, text: string) => { return null; };
export const generateChatCompletion = async (token: string = '', body: object) => { return [null, null]; };
export const unloadModel = async (token: string, tagName: string) => { return null; };
export const createModel = async (token: string, payload: object, urlIdx: string | null = null) => { return null; };
export const deleteModel = async (token: string, tagName: string, urlIdx: string | null = null) => { return null; };
export const pullModel = async (token: string, tagName: string, urlIdx: number | null = null) => { return [null, null]; };
export const downloadModel = async (token: string, download_url: string, urlIdx: string | null = null) => { return null; };
export const uploadModel = async (token: string, file: File, urlIdx: string | null = null) => { return null; };
