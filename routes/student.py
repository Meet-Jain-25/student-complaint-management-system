from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash
)

from flask_login import login_required, current_user

from extensions import db
from models.complaint import Complaint


student_bp = Blueprint(
    "student",
    __name__,
    url_prefix="/student"
)


@student_bp.route("/dashboard")
@login_required
def dashboard():
    complaints = (
        db.session.execute(
            db.select(Complaint)
            .where(Complaint.student_id == current_user.id)
            .order_by(Complaint.created_at.desc())
        )
        .scalars()
        .all()
    )

    total = len(complaints)

    pending = sum(
        1 for complaint in complaints
        if complaint.status == "Pending"
    )

    in_progress = sum(
        1 for complaint in complaints
        if complaint.status == "In Progress"
    )

    resolved = sum(
        1 for complaint in complaints
        if complaint.status in ["Resolved", "Closed"]
    )

    return render_template(
        "student/dashboard.html",
        complaints=complaints,
        total=total,
        pending=pending,
        in_progress=in_progress,
        resolved=resolved
    )


@student_bp.route("/complaint/new", methods=["GET", "POST"])
@login_required
def new_complaint():

    if request.method == "POST":

        title = request.form.get(
            "title",
            ""
        ).strip()

        category = request.form.get(
            "category",
            ""
        ).strip()

        description = request.form.get(
            "description",
            ""
        ).strip()

        priority = request.form.get(
            "priority",
            "Medium"
        ).strip()

        if not title or not category or not description:
            flash(
                "Please fill in all required fields.",
                "error"
            )

            return render_template(
                "student/new_complaint.html"
            )

        complaint = Complaint(
            student_id=current_user.id,
            title=title,
            category=category,
            description=description,
            priority=priority,
            status="Pending"
        )

        db.session.add(complaint)
        db.session.commit()

        flash(
            "Your complaint has been submitted successfully.",
            "success"
        )

        return redirect(
            url_for("student.dashboard")
        )

    return render_template(
        "student/new_complaint.html"
    )


@student_bp.route("/complaint/<int:complaint_id>")
@login_required
def view_complaint(complaint_id):

    complaint = db.get_or_404(
        Complaint,
        complaint_id
    )

    # Security check:
    # A student can only view their own complaints.
    if complaint.student_id != current_user.id:

        flash(
            "You are not authorized to view this complaint.",
            "error"
        )

        return redirect(
            url_for("student.dashboard")
        )

    return render_template(
        "student/view_complaint.html",
        complaint=complaint
    )