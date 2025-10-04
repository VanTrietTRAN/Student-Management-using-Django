export interface Student {
    id: number;
    studentId: string;
    fullName: string;
    email: string;
    phone: string;
    class: string;
    major: string;
    status: 'Đang học' | 'Tốt nghiệp' | 'Tạm nghỉ';
    gpa: number;
    profile_picture?: string | File | null;
    profile_picture_preview?: string | null;
}

export interface NewStudent {
    studentId: string;
    fullName: string;
    email: string;
    phone: string;
    class: string;
    major: string;
    profile_picture?: File | null;
    profile_picture_preview?: string | null;
}

export interface EditingStudent extends Student {
    profile_picture?: File | string | null;
    profile_picture_preview?: string | null;
}