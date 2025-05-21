import { Toaster } from "sonner";

// Toast notification component using sonner
const Toast = () => {
  return (
    <Toaster 
      position="top-right"
      toastOptions={{
        className: "toast-custom",
        style: {
          background: 'var(--background)',
          color: 'var(--foreground)',
          border: '1px solid var(--border)',
          boxShadow: '0 2px 10px rgba(0, 0, 0, 0.08)',
        },
      }}
    />
  );
};

export { Toast };