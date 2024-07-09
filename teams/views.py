from datetime import datetime
from rest_framework.views import APIView, Response, status
from teams.models import Team
from django.forms.models import model_to_dict
from exceptions import (
    NegativeTitlesError,
    ImpossibleTitlesError,
    InvalidYearCupError,
)


class TeamView(APIView):
    def post(self, request):
        data = request.data
        world_cup_years_list = [n for n in range(1930, 2024, 4)]

        try:
            if data["titles"] < 0:
                raise NegativeTitlesError

            date_obj = datetime.strptime(data["first_cup"], "%Y-%m-%d")
            year = date_obj.year
            if world_cup_years_list.count(year) != 1:
                raise InvalidYearCupError

            max_titles = [n for n in range(year, 2024, 4)]
            if len(max_titles) < data["titles"]:
                raise ImpossibleTitlesError

            team = Team.objects.create(
                name=data["name"],
                titles=(data["titles"]),
                top_scorer=data["top_scorer"],
                fifa_code=data["fifa_code"],
                first_cup=data["first_cup"],
            )
            return Response(model_to_dict(team), status.HTTP_201_CREATED)
        except NegativeTitlesError as e:
            return Response({"error": e.message}, status.HTTP_400_BAD_REQUEST)
        except InvalidYearCupError as e:
            return Response({"error": e.message}, status.HTTP_400_BAD_REQUEST)
        except ImpossibleTitlesError as e:
            return Response({"error": e.message}, status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        teams = Team.objects.all()

        teams_dict = []

        for team in teams:
            transformed_team = model_to_dict(team)
            teams_dict.append(transformed_team)

        return Response(teams_dict, status.HTTP_200_OK)


class TeamDetailView(APIView):
    def get(self, request, team_id):
        try:
            team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"},
                status.HTTP_404_NOT_FOUND,
            )
        return Response(model_to_dict(team), status.HTTP_200_OK)

    def patch(self, request, team_id):
        try:
            team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"},
                status.HTTP_404_NOT_FOUND,
            )
        request_keys = list(request.data.keys())
        request_values = list(request.data.values())

        for i in range(0, len(request_keys)):
            setattr(team, request_keys[i], request_values[i])

        team.save()
        return Response(model_to_dict(team), status.HTTP_200_OK)

    def delete(self, request, team_id):
        try:
            Team.objects.get(pk=team_id).delete()
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"},
                status.HTTP_404_NOT_FOUND,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
