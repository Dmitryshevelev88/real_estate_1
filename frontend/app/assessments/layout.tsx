import AuthGuard from "@/components/AuthGuard";
import Navbar from "@/components/Navbar";

export default function AssessmentsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <AuthGuard>
      <div className="min-h-screen bg-slate-50">
        <Navbar />
        {children}
      </div>
    </AuthGuard>
  );
}