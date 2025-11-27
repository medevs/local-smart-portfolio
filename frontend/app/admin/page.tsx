"use client";

import { useState, useEffect, useCallback } from "react";
import { motion } from "framer-motion";
import {
  Upload,
  FileText,
  Trash2,
  Database,
  RefreshCw,
  CheckCircle,
  XCircle,
  Loader2,
  Shield,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { api, DocumentInfo, KBStats, HealthStatus } from "@/lib/api";

/**
 * Admin Dashboard Page
 * Route: /admin
 * 
 * Allows managing the RAG knowledge base:
 * - Upload documents (PDF, MD, TXT, DOCX)
 * - View uploaded documents
 * - Delete documents
 * - View system health status
 */
export default function AdminPage() {
  // State
  const [documents, setDocuments] = useState<DocumentInfo[]>([]);
  const [stats, setStats] = useState<KBStats | null>(null);
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // Fetch all data
  const fetchData = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const [healthData, docsData, statsData] = await Promise.all([
        api.getHealth().catch(() => null),
        api.getDocuments().catch(() => []),
        api.getStats().catch(() => null),
      ]);
      
      setHealth(healthData);
      setDocuments(docsData);
      setStats(statsData);
    } catch (err) {
      setError("Failed to connect to backend. Make sure it's running on port 8000.");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // Handle file upload
  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    setUploadProgress(0);
    setError(null);
    setSuccess(null);

    // Simulate progress (real progress would need backend support)
    const progressInterval = setInterval(() => {
      setUploadProgress((prev) => Math.min(prev + 10, 90));
    }, 200);

    try {
      const result = await api.uploadDocument(file);
      
      clearInterval(progressInterval);
      setUploadProgress(100);
      
      if (result.success) {
        setSuccess(`Document "${file.name}" uploaded successfully! (${result.document?.chunk_count || 0} chunks)`);
        fetchData(); // Refresh the list
      } else {
        setError(result.message || result.error || "Upload failed");
      }
    } catch (err) {
      clearInterval(progressInterval);
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setIsUploading(false);
      setUploadProgress(0);
      // Reset the input
      event.target.value = "";
    }
  };

  // Handle document deletion
  const handleDelete = async (documentId: string, filename: string) => {
    if (!confirm(`Are you sure you want to delete "${filename}"?`)) return;

    setError(null);
    setSuccess(null);

    try {
      await api.deleteDocument(documentId);
      setSuccess(`Document "${filename}" deleted successfully`);
      fetchData(); // Refresh the list
    } catch (err) {
      setError(err instanceof Error ? err.message : "Delete failed");
    }
  };

  // Format file size
  const formatSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  // Format date
  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-8"
    >
      {/* Header */}
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-amber-100 mb-4 flex items-center justify-center gap-3">
          <Shield className="w-10 h-10 text-amber-500" />
          Admin Dashboard
        </h1>
        <p className="text-lg text-amber-200/70 max-w-2xl mx-auto">
          Manage your RAG knowledge base - upload, view, and delete documents
        </p>
      </div>

      {/* Status Messages */}
      {error && (
        <div className="bg-red-900/30 border border-red-700 rounded-lg p-4 flex items-center gap-3">
          <XCircle className="w-5 h-5 text-red-400" />
          <span className="text-red-200">{error}</span>
        </div>
      )}
      {success && (
        <div className="bg-green-900/30 border border-green-700 rounded-lg p-4 flex items-center gap-3">
          <CheckCircle className="w-5 h-5 text-green-400" />
          <span className="text-green-200">{success}</span>
        </div>
      )}

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Health Status */}
        <Card className="bg-gradient-to-br from-amber-950/40 to-amber-900/20 border-amber-700/30">
          <CardHeader className="pb-2">
            <CardTitle className="text-amber-100 text-lg flex items-center gap-2">
              <Database className="w-5 h-5 text-amber-500" />
              System Status
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-amber-200/70">Backend</span>
              {health ? (
                <Badge className="bg-green-600">Connected</Badge>
              ) : (
                <Badge variant="destructive">Disconnected</Badge>
              )}
            </div>
            <div className="flex items-center justify-between">
              <span className="text-amber-200/70">Ollama</span>
              {health?.services?.ollama === "connected" ? (
                <Badge className="bg-green-600">Online</Badge>
              ) : (
                <Badge variant="destructive">Offline</Badge>
              )}
            </div>
            <div className="flex items-center justify-between">
              <span className="text-amber-200/70">ChromaDB</span>
              {health?.services?.chromadb === "connected" ? (
                <Badge className="bg-green-600">Online</Badge>
              ) : (
                <Badge variant="destructive">Offline</Badge>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Document Stats */}
        <Card className="bg-gradient-to-br from-amber-950/40 to-amber-900/20 border-amber-700/30">
          <CardHeader className="pb-2">
            <CardTitle className="text-amber-100 text-lg flex items-center gap-2">
              <FileText className="w-5 h-5 text-amber-500" />
              Knowledge Base
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-amber-200/70">Documents</span>
              <span className="text-2xl font-bold text-amber-100">
                {stats?.total_documents ?? documents.length}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-amber-200/70">Total Chunks</span>
              <span className="text-2xl font-bold text-amber-100">
                {stats?.total_chunks ?? 0}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-amber-200/70">Embedding</span>
              <span className="text-amber-100 text-xs font-mono truncate max-w-32">
                {stats?.embedding_model || "N/A"}
              </span>
            </div>
          </CardContent>
        </Card>

        {/* Upload Card */}
        <Card className="bg-gradient-to-br from-amber-950/40 to-amber-900/20 border-amber-700/30">
          <CardHeader className="pb-2">
            <CardTitle className="text-amber-100 text-lg flex items-center gap-2">
              <Upload className="w-5 h-5 text-amber-500" />
              Upload Document
            </CardTitle>
            <CardDescription className="text-amber-200/60">
              PDF, MD, TXT, DOCX (max 10MB)
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <Input
                type="file"
                accept=".pdf,.md,.txt,.docx"
                onChange={handleFileUpload}
                disabled={isUploading}
                className="bg-amber-950/30 border-amber-700/50 text-amber-100 file:bg-amber-700 file:text-white file:border-0 file:mr-4"
              />
              {isUploading && (
                <div className="space-y-2">
                  <Progress value={uploadProgress} className="h-2 bg-amber-950/50" />
                  <p className="text-xs text-amber-200/60 flex items-center gap-2">
                    <Loader2 className="w-3 h-3 animate-spin" />
                    Uploading and processing...
                  </p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Documents List */}
      <Card className="bg-gradient-to-br from-amber-950/40 to-amber-900/20 border-amber-700/30">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-amber-100 flex items-center gap-2">
                <FileText className="w-5 h-5 text-amber-500" />
                Uploaded Documents
              </CardTitle>
              <CardDescription className="text-amber-200/60">
                Documents in your RAG knowledge base
              </CardDescription>
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={fetchData}
              disabled={isLoading}
              className="border-amber-700/50 text-amber-200 hover:bg-amber-900/30"
            >
              <RefreshCw className={`w-4 h-4 mr-2 ${isLoading ? "animate-spin" : ""}`} />
              Refresh
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="w-8 h-8 animate-spin text-amber-500" />
            </div>
          ) : documents.length === 0 ? (
            <div className="text-center py-8 text-amber-200/60">
              <FileText className="w-12 h-12 mx-auto mb-3 opacity-50" />
              <p>No documents uploaded yet</p>
              <p className="text-sm mt-1">Upload your first document to get started</p>
            </div>
          ) : (
            <div className="space-y-3">
              {documents.map((doc) => (
                <motion.div
                  key={doc.document_id}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="flex items-center justify-between p-4 rounded-lg bg-amber-950/30 border border-amber-800/30 hover:border-amber-700/50 transition-colors"
                >
                  <div className="flex items-center gap-4">
                    <FileText className="w-8 h-8 text-amber-500" />
                    <div>
                      <p className="font-medium text-amber-100">{doc.filename}</p>
                      <div className="flex items-center gap-3 text-sm text-amber-200/60">
                        <span>{formatSize(doc.file_size)}</span>
                        <span>•</span>
                        <span>{doc.chunk_count} chunks</span>
                        <span>•</span>
                        <span>{formatDate(doc.uploaded_at)}</span>
                      </div>
                    </div>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleDelete(doc.document_id, doc.filename)}
                    className="text-red-400 hover:text-red-300 hover:bg-red-900/30"
                  >
                    <Trash2 className="w-4 h-4" />
                  </Button>
                </motion.div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
}

