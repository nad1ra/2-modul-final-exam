from .models import Group
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from teachers.models import Teacher
from subjects.models import Subject



class GroupListView(ListView):
    model = Group
    template_name = 'groups/list.html'
    context_object_name = 'groups'
    paginate_by = 10

    def get_queryset(self):
        groups = Group.objects.all()
        grade_level_filter = self.request.GET.get('grade_level')
        class_teacher_filter = self.request.GET.get('class_teacher')
        status = self.request.GET.get('status')
        search_query = self.request.GET.get('search')


        if grade_level_filter:
            groups = groups.filter(grade_level_id=grade_level_filter)

        if class_teacher_filter:
            groups = groups.filter(class_teacher_id=class_teacher_filter)


        if status:
            groups = groups.filter(status=status)


        if search_query:
            groups = groups.filter(name__icontains=search_query)

        return groups

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['class_teacher'] = Teacher.objects.all()
        context['subjects'] = Subject.objects.all()

        return context


class GroupCreateView(CreateView):
    model = Group
    template_name = 'groups/form.html'
    fields = ['name', 'class_teacher', 'academic_year', 'grade_level', 'schedule', 'max_students', 'description', 'subjects']
    success_url = reverse_lazy('group_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'class_teacher': Teacher.objects.filter}


class GroupDetailView(DetailView):
    model = Group
    template_name = 'groups/detail.html'
    context_object_name = 'group'


class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'groups/form.html'
    fields = ['name', 'class_teacher', 'academic_year', 'grade_level', 'schedule', 'max_students', 'description', 'subjects']
    success_url = reverse_lazy('group_list')

class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'groups/delete-confirm.html'
    success_url = reverse_lazy('group_list')

