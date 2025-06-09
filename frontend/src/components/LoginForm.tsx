import { TextField, Button, Stack, Alert, CircularProgress } from '@mui/material';
import { useForm } from 'react-hook-form';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import type { LoginCredentials } from '../types/user';
import AuthService from '../services/auth';
import { ApiError } from '../services/api';

type FormValues = LoginCredentials;

interface LoginFormProps {
  onLoginSuccess?: (userId: number) => void;
}

function LoginForm({ onLoginSuccess }: LoginFormProps) {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    
    const form = useForm<FormValues>({
        defaultValues: {
            email: '',
            password: '',
        },
    });

    const { register, handleSubmit, formState } = form;
    const { errors } = formState;

    const formSubmit = async (data: FormValues) => {
        try {
            setLoading(true);
            setError(null);
            
            // Call the actual FastAPI backend
            const response = await AuthService.login(data);
            
            console.log('Login successful:', response);
            
            if (onLoginSuccess) {
                onLoginSuccess(response.user.id);
            } else {
                // Navigate to profile page
                navigate(`/profile/${response.user.id}`);
            }
            
        } catch (err) {
            console.error('Login error:', err);
            
            if (err instanceof ApiError) {
                // Handle specific API errors
                if (err.status === 401) {
                    setError('Invalid email or password. Please try again.');
                } else if (err.status === 0) {
                    setError('Unable to connect to server. Please check your connection.');
                } else {
                    setError(err.message || 'Login failed. Please try again.');
                }
            } else {
                setError('An unexpected error occurred. Please try again.');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            <h1>Welcome to your portal</h1>
            <p style={{ marginBottom: '16px', color: '#666', textAlign: 'center' }}>
                Please enter your credentials to access your profile
            </p>
            {error && (
                <Alert severity="error" sx={{ mb: 2, width: 400 }}>
                    {error}
                </Alert>
            )}
            <form onSubmit={handleSubmit(formSubmit)} noValidate>
                <Stack spacing={2} width={400}>
                    <TextField
                        label="Email"
                        type="email"
                        variant="outlined"
                        fullWidth
                        disabled={loading}
                        {...register('email', 
                            { required: 'Email is required', 
                              pattern: {
                                value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                                message: 'Invalid email address',
                            }
                        })}
                        error={!!errors.email}
                        helperText={errors.email ? errors.email.message : ''}
                    />
                    <TextField
                        label="Password"
                        type="password"
                        variant="outlined"
                        fullWidth
                        disabled={loading}
                        {...register('password', { required: 'Password is required' })}
                        error={!!errors.password}
                        helperText={errors.password ? errors.password.message : ''}
                    />
                    <Button 
                        variant="contained" 
                        color="primary" 
                        type="submit"
                        disabled={loading}
                        startIcon={loading ? <CircularProgress size={20} /> : null}
                    >
                        {loading ? 'Logging in...' : 'Login'}
                    </Button>
                </Stack>
            </form>
        </>
    )
}

export default LoginForm;