export interface Teacher {
    id: number;
    teacherId: string;
    fullName: string;
    email: string;
    phone: string;
    department: string;
    status: 'Đang làm việc' | 'Nghỉ việc' | 'Tạm nghỉ';
    profile_picture?: string | File | null;
    profile_picture_preview?: string | null;
}

export interface NewTeacher {
    teacherId: string;
    fullName: string;
    email: string;
    phone: string;
    department: string;
    profile_picture?: File | null;
    profile_picture_preview?: string | null;
}

export interface EditingTeacher extends Teacher {
    profile_picture?: File | string | null;
    profile_picture_preview?: string | null;
}